from pathlib import Path
from typing import List, Literal, Optional, Tuple, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog

from ....api.joc.http.v_2_6_5.agents.import_ import import_, EndpointCall, Options as Options_V_2_6_5
from ....util.version_to_tuple import version_to_tuple
from ....util.detect_archive_type import detect_archive_type
from ....util.bytes_converter.files_to_bytes import files_to_bytes
from ....util.bytes_converter.bytes_to_archive_bytes import bytes_to_archive_bytes
from ....util.bytes_converter.read_bytes_archive_files_to_bytes import read_bytes_archive_files_to_bytes


def import_agents_action(
    *, 
    context: Context,
    controller_id: str,
    file_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    overwrite: bool,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        options, data = _build_v_2_6_5_request(
            controller_id=controller_id,
            file_path=Path(file_path),
            archive_format=archive_format,
            overwrite=overwrite,
            audit_log=audit_log
        )

        result = import_(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=data,
            options=options
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    file_path: Path,
    archive_format: Literal["ZIP", "TAR_GZ"],
    overwrite: bool,
    audit_log: Optional[AuditLog]
) -> Tuple[Options_V_2_6_5, bytes]:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
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
    
    # Build: res_files
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
    
    # Build: res_archive
    res_archive = bytes_to_archive_bytes(archive_format=archive_format, files=files)
    
    # Build: options
    res_options: Options_V_2_6_5 = {
        "format": archive_format,
        "overwrite": overwrite,
        "controller_id": controller_id,
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
