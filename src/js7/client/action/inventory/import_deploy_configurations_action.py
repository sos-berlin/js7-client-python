from pathlib import Path
from typing import List, Literal, Optional, Tuple, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend

from ...client import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.inventory.deployment.import_deploy import import_deploy, EndpointCall, Options
from ....util.version_to_tuple import version_to_tuple

from ....util.bytes_converter.bytes_to_archive_bytes import bytes_to_archive_bytes
from ....util.bytes_converter.read_bytes_archive_files_to_bytes import read_bytes_archive_files_to_bytes
from ....util.bytes_converter.files_to_bytes import files_to_bytes
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
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        options, archive = _build_v_2_6_5_request(
            controller_id=controller_id,
            file_path=Path(file_path),
            archive_format=archive_format,
            private_key_file=Path(private_key_file),
            public_key_file=Path(public_key_file) if public_key_file else None,
            key_password=key_password,
            hash_alg=hash_alg,
            audit_log=audit_log
        )

        result = import_deploy(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=archive,
            options=options
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

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

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    file_path: Path,
    archive_format: Literal["ZIP", "TAR_GZ"],
    private_key_file: Path,
    public_key_file: Optional[Path],
    key_password: Optional[bytes],
    hash_alg: hashes.HashAlgorithm,
    audit_log: Optional[AuditLog]
) -> Tuple[Options, bytes]:
    
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
        
        path = "/" + path
        
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
            
            # Removes the archive name from path
            path = "/".join(path.split("/")[:-1])

            for arch_path, arch_file in arch_files:
                # Skips invalid filenames
                if arch_path.rsplit("/", 1)[-1].startswith((".", "_", "-")):
                    continue
                
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
    res_options: Options = {
        "controller_id": controller_id,
        "signature_algorithm": get_signature_alg(
            private_key_file=private_key_file, 
            key_password=key_password,
            hash_alg=hash_alg
        ),
        "format": archive_format,
        "audit_log_comment": None,
        "audit_log_ticket_link": None,
        "audit_log_time_spent": None
    }
    
    # Build: audit_log
    if audit_log:
        if audit_log.ticket_link:
            res_options["audit_log_ticket_link"] = audit_log.ticket_link
        if audit_log.comment:
            res_options["audit_log_comment"] = audit_log.comment
        if audit_log.time_spent:
            res_options["audit_log_time_spent"] = str(audit_log.time_spent)
    
    # Result
    return res_options, res_archive
