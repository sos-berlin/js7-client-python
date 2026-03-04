from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend

from ...client import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_8_2 import OK as OK_V_2_8_2
from ....model.private.api.endpoint import EndpointCall

from ....util.bytes_converter.bytes_to_archive_bytes import bytes_to_archive_bytes
from ....util.bytes_converter.read_bytes_archive_files_to_bytes import read_bytes_archive_files_to_bytes
from ....util.bytes_converter.files_to_bytes import files_to_bytes
from ....util.check_matching_version import check_matching_version
from ....util.detect_archive_type import detect_archive_type
from ....util.bytes_converter.sign_to_bytes import sign_to_bytes


def import_deploy_configurations_action(
    *,
    context: Context,
    controller_id: str,
    file_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    private_key_file: Union[Path, str],
    public_key_file: Optional[Union[Path, str]],
    key_password: Optional[bytes],
    hash_alg: hashes.HashAlgorithm,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        options, archive = _build_v_2_8_2_request(
            controller_id=controller_id,
            file_path=Path(file_path),
            archive_format=archive_format,
            private_key_file=Path(private_key_file),
            public_key_file=Path(public_key_file) if public_key_file else None,
            key_password=key_password,
            hash_alg=hash_alg,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/deployment/import_deploy", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=archive,
        options=options
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

def get_signature_alg(
    private_key_file: Path,
    key_password: Optional[bytes],
    hash_alg: hashes.HashAlgorithm,
) -> str:

    with open(private_key_file, "rb") as f:
        key = serialization.load_pem_private_key(
            f.read(),
            password=key_password,
            backend=default_backend(),
        )

    if isinstance(key, rsa.RSAPrivateKey):
        key_part = "RSA"
    elif isinstance(key, ec.EllipticCurvePrivateKey):
        key_part = "ECDSA"
    else:
        raise TypeError("Only RSA and ECDSA private keys are supported")

    return f"{hash_alg.name.upper()}with{key_part}"

#-------------------------------#
# Build 2.8.2 request           #
# Returns: [Formdata, Aarchive] #
#-------------------------------#
def _build_v_2_8_2_request(
    *,
    controller_id: str,
    file_path: Path,
    archive_format: Literal["ZIP", "TAR_GZ"],
    private_key_file: Path,
    public_key_file: Optional[Path],
    key_password: Optional[bytes],
    hash_alg: hashes.HashAlgorithm,
    audit_log: Optional[AuditLog]
) -> Tuple[Dict[str, Any], bytes]:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError(f"'controller_id' is required.")
    
    # Validate: file_path
    if not file_path.exists():
        raise ValueError(f"File path does not exist: {file_path}")
    
    # Validate: archive_format
    if archive_format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'archive_format' must be 'ZIP' or 'TAR_GZ'.")
    
    # Build: files_as_bytes
    files_as_bytes = files_to_bytes(
        file_path=file_path,
        filter_suffixes=[".json", ".zip", ".tar.gz", ".tgz"]
    )
    
    if not files_as_bytes:
        raise ValueError(
            "No matching files found for import. "
            "Expected: '*.json', '*.zip', '*.tar.gz', '*.tgz'."
        )
    
    # Build: files
    files: List[Tuple[str, bytes]] = []
    
    for path, file in files_as_bytes:
        # Skips invalid filenames
        if path.rsplit("/", 1)[-1].startswith((".", "_", "-")):
            continue
                
        archive_type = detect_archive_type(file)
        
        if not archive_type and path.endswith(".json"):
            files.append((path, file))
        else:
            arch_files = read_bytes_archive_files_to_bytes(
                file=file, 
                filter_suffixes=[".json"]
            )
            
            if not arch_files:
                continue
            
            for arch_path, arch_file in arch_files:
                # Skips invalid filenames
                if arch_path.rsplit("/", 1)[-1].startswith((".", "_", "-")):
                    continue
                
                # Removes archive suffix
                path = path.split(".")[0]
                
                new_path = path + "/" + arch_path
                files.append((new_path, arch_file))
    
    # Build: Signing
    files.extend(sign_to_bytes(
        files=files,
        private_key_file=private_key_file,
        public_key_file=public_key_file,
        key_password=key_password,
        hash_alg=hash_alg
    ))
    
    # Build: res_archive
    res_archive = bytes_to_archive_bytes(archive_format=archive_format, files=files)
    
    # Build: options
    res_options: Dict[str, Any] = {
        "controller_id": controller_id,
        "signature_algorithm": get_signature_alg(
            private_key_file=private_key_file, 
            key_password=key_password,
            hash_alg=hash_alg
        ),
        "format": archive_format, 
    }
    
    # Build: audit_log
    if audit_log:
        if audit_log.ticket_link:
            res_options["audit_log_ticket_link"] = audit_log.ticket_link
        if audit_log.comment:
            res_options["audit_log_comment"] = audit_log.comment
        if audit_log.time_spent:
            res_options["audit_log_time_spent"] = audit_log.time_spent
    
    # Result
    return res_options, res_archive
