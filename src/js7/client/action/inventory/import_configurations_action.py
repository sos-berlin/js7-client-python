from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from ...client import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_8_2 import OK as OK_V_2_8_2
from ....model.private.api.endpoint import EndpointCall

from ....util.bytes_converter.bytes_to_archive_bytes import bytes_to_archive_bytes
from ....util.bytes_converter.read_bytes_archive_files_to_bytes import read_bytes_archive_files_to_bytes
from ....util.bytes_converter.files_to_bytes import files_to_bytes
from ....util.check_matching_version import check_matching_version
from ....util.detect_archive_type import detect_archive_type


def import_configurations_action(
    *,
    context: Context,
    file_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    overwrite: bool,
    inventory_target_folder: Optional[str],
    suffix: Optional[str],
    prefix: Optional[str],
    overwrite_tags: bool,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        options, archive = _build_v_2_8_2_request(
            file_path=Path(file_path),
            archive_format=archive_format,
            overwrite=overwrite,
            inventory_target_folder=inventory_target_folder,
            suffix=suffix,
            prefix=prefix,
            overwrite_tags=overwrite_tags,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/import", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=archive,
        options=options
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------------------------#
# Build 2.8.2 request                   #
# Returns: [Formdata, List of archives] #
#---------------------------------------#
def _build_v_2_8_2_request(
    *,
    file_path: Path,
    archive_format: Literal["ZIP", "TAR_GZ"],
    overwrite: bool,
    inventory_target_folder: Optional[str],
    suffix: Optional[str],
    prefix: Optional[str],
    overwrite_tags: bool,
    audit_log: Optional[AuditLog]
) -> Tuple[Dict[str, Any], bytes]:
    
    # Validate: file_path
    if not file_path.exists():
        raise ValueError(f"File path does not exist: {file_path}")
    
    # Validate: archive_format
    if archive_format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'archive_format' must be 'ZIP' or 'TAR_GZ'.")
    
    # Validate: inventory_target_folder
    if inventory_target_folder and not inventory_target_folder.startswith("/"):
        inventory_target_folder = "/" + inventory_target_folder
    
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
    
    # Build: res_archive
    res_archive = bytes_to_archive_bytes(archive_format=archive_format, files=files)
    
    # Build: options
    res_options: Dict[str, Any] = {
        "format": archive_format,
        "overwrite": overwrite,
        "overwrite_tags": overwrite_tags    
    }
    
    if inventory_target_folder:
        res_options["target_folder"] = inventory_target_folder
    
    if suffix:
        res_options["suffix"] = suffix
    
    if prefix:
        res_options["prefix"] = prefix
    
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
