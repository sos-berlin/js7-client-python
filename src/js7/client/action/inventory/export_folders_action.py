from pathlib import Path
from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.enum.object_types import DeployObjectType, ReleaseObjectType
from ....model.public.client.filter.export_folders_filter import ExportFoldersFilter
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    ArchiveFormat as ArchiveFormat_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    ExportFile as ExportFile_V_2_8_2,
    ExportFolderFilter as ExportFolderFilter_V_2_8_2,
    ExportFolderForSigning as ExportFolderForSigning_V_2_8_2,
    ShallowCopy as ShallowCopy_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def export_folders_action(
    *,
    context: Context,
    controller_id: str,
    out_dir: Union[Path, str],
    filename: str,
    archive_format: Literal["ZIP", "TAR_GZ"],
    filter: ExportFoldersFilter,
    audit_log: Optional[AuditLog]
) -> bool:

    # Normalize out_path
    out_dir = Path(out_dir)

    # Determine expected suffix from archive_format
    expected_suffix = ".tar.gz" if archive_format == "TAR_GZ" else ".zip"
    
    # Append suffix if missing or wrong
    if not filename.endswith((".zip", ".tar.gz")):
        filename = filename + expected_suffix
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            out_dir=out_dir,
            filename=filename,
            archive_format=archive_format,
            filter=filter,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    result = context.joc_api.dispatch(endpoint_id="inventory/export/folder", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, bytes):    
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / filename
        out_file.write_bytes(result)
        return out_file.exists()
        
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    controller_id: str,
    out_dir: Path,
    filename: str,
    archive_format: Literal["ZIP", "TAR_GZ"],
    filter: ExportFoldersFilter,
    audit_log: Optional[AuditLog]
) -> ExportFolderFilter_V_2_8_2:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: out_dir
    if not out_dir.is_dir():
        raise ValueError("'out_dir' must be a directory.")
    
    # Validate: filename
    if not filename:
        raise ValueError("'filename' is required.")
    
    # Validate: archive_format
    if archive_format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'archive_format' must be 'ZIP' or 'TAR_GZ'.")
    
    # Validate: folder_paths
    if not filter.folder_paths:
        raise ValueError("At least one folder path in 'folder_paths' is required")
    
    # Build: object_types - Default: All object types.
    res_object_types: List[ConfigurationType_V_2_8_2] = []
    if filter.object_types:
        for obj_type in filter.object_types:
            res_object_types.append(ConfigurationType_V_2_8_2(obj_type.value)) # Raises ValueError() if invalid
    elif filter.for_signing:
        for obj_type in DeployObjectType:
            res_object_types.append(ConfigurationType_V_2_8_2(obj_type.value)) # Raises ValueError() if invalid
    else:
        for obj_type in ReleaseObjectType:
            res_object_types.append(ConfigurationType_V_2_8_2(obj_type.value)) # Raises ValueError() if invalid
            
        for obj_type in DeployObjectType:
            try:
                ReleaseObjectType(obj_type.value)  # exists -> skip
            except ValueError:
                res_object_types.append(ConfigurationType_V_2_8_2(obj_type.value)) # Raises ValueError() if invalid
    
    # Build: for_signing_result and shallow_copy_result
    for_signing_result: Optional[ExportFolderForSigning_V_2_8_2] = None
    shallow_copy_result: Optional[ShallowCopy_V_2_8_2] = None
    if filter.for_signing is True:    
        for_signing_result = ExportFolderForSigning_V_2_8_2(
            controller_id=controller_id,
            folders=filter.folder_paths,
            object_types=res_object_types,
            recursive=True,
            without_deployed=filter.no_deployed,
            without_drafts=filter.no_draft,
        )
    else:
        shallow_copy_result = ShallowCopy_V_2_8_2(
            folders=filter.folder_paths,
            object_types=res_object_types,
            incl_all_tags=True,
            only_valid_objects=filter.no_invalid,
            recursive=filter.recursive,
            without_deployed=filter.no_deployed,
            without_drafts=filter.no_draft,
            without_released=filter.no_released,
        )
        
    # Build: audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    return ExportFolderFilter_V_2_8_2(
        export_file=ExportFile_V_2_8_2(
            filename=filename,
            format=ArchiveFormat_V_2_8_2(archive_format)
        ),
        for_signing=for_signing_result,
        shallow_copy=shallow_copy_result,
        use_short_path=filter.use_short_path,
        audit_log=res_audit_log
    )
