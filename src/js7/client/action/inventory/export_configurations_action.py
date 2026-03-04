from pathlib import Path
from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import DraftConfiguration, DeployConfiguration
from ....model.public.client.filter.export_filter import ExportFilter
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    PublishConfiguration as Configuration_V_2_8_2,
    ExportFilter as ExportFilter_V_2_8_2,
    ExportForSigning as ExportForSigning_V_2_8_2,
    DeployablesValidFilter as DeployablesValidFilter_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    Config as Config_V_2_8_2,
    ExportFile as ExportFile_V_2_8_2,
    ArchiveFormat as ArchiveFormat_V_2_8_2,
    ExportShallowCopy as ExportShallowCopy_V_2_8_2,
    DeployablesFilter as DeployablesFilter_V_2_8_2,
    ReleasablesFilter as ReleasablesFilter_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2
)

from ....util.check_matching_version import check_matching_version
from ....util.bytes_converter.bytes_to_file import bytes_to_file


def export_configurations_action(
    *,
    context: Context,
    controller_id: str,
    out_dir: Union[Path, str],
    filename: str,
    archive_format: Literal["ZIP", "TAR_GZ"],
    filter: ExportFilter,
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
    
    result = context.joc_api.dispatch(endpoint_id="inventory/export", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, bytes):
        return bytes_to_file(data=result, out_path=Path(out_dir / filename))

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    controller_id: str,
    out_dir: Path,
    filename: str,
    archive_format: Literal["ZIP", "TAR_GZ"],
    filter: ExportFilter,
    audit_log: Optional[AuditLog]
) -> ExportFilter_V_2_8_2:
    
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
    
    # Validate: filter.configurations
    if not filter.configurations:
        raise ValueError("At least one configuration must be provided.")
    
    # Build: export_file
    res_export_file = ExportFile_V_2_8_2(
        filename=Path(out_dir / filename).name,
        format=(ArchiveFormat_V_2_8_2(archive_format)) # Raises ValueError() if invalid.
    )
    
    # Build: configurations
    res_draft_configurations: Optional[List[Config_V_2_8_2]] = None
    res_deploy_configurations: Optional[List[Config_V_2_8_2]] = None
    res_release_configurations: Optional[List[Config_V_2_8_2]] = None
    for config in filter.configurations:
        if isinstance(config, DraftConfiguration):
            if not res_draft_configurations:
                res_draft_configurations = []
            
            res_draft_configurations.append(
                Config_V_2_8_2(
                    configuration=Configuration_V_2_8_2(
                        object_type=ConfigurationType_V_2_8_2(config.object_type), # Raises ValueError() if invalid.
                        path=config.path,
                        recursive=config.recursive
                    )
                )
            )
            
            continue
            
        if isinstance(config, DeployConfiguration):
            if not res_deploy_configurations:
                res_deploy_configurations = []
                
            res_deploy_configurations.append(
                Config_V_2_8_2(
                    configuration=Configuration_V_2_8_2(
                        commit_id=config.commit_id,
                        object_type=ConfigurationType_V_2_8_2(config.object_type), # Raises ValueError() if invalid.
                        path=config.path,
                        recursive=config.recursive
                    )
                )
            )
            
            continue
        
        else:
            if not res_release_configurations:
                res_release_configurations = []
                
            res_release_configurations.append(
                Config_V_2_8_2(
                    configuration=Configuration_V_2_8_2(
                        object_type=ConfigurationType_V_2_8_2(config.object_type), # Raises ValueError() if invalid.
                        path=config.path,
                        recursive=config.recursive
                    )
                )
            )
    
    # Build: for_signing
    res_for_signing = ExportForSigning_V_2_8_2(
        controller_id=controller_id,
        deployables=DeployablesValidFilter_V_2_8_2(
            deploy_configurations=res_deploy_configurations,
            draft_configurations=res_draft_configurations
        )
    ) if filter.for_signing is True else None
        
    # Build: shallow_copy
    res_shallow_copy = ExportShallowCopy_V_2_8_2(
        incl_all_tags=filter.include_all_tags,
        deployables=DeployablesFilter_V_2_8_2(
            without_invalid=filter.without_invalid_drafts,
            draft_configurations=res_draft_configurations,
            deploy_configurations=res_deploy_configurations
        ),
        releasables=ReleasablesFilter_V_2_8_2(
            without_invalid=filter.without_invalid_drafts,
            draft_configurations=res_draft_configurations,
            released_configurations=res_release_configurations
        ) if (res_draft_configurations or res_release_configurations) else None
    ) if filter.for_signing is False else None

    # Build: audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ExportFilter_V_2_8_2(
        export_file=res_export_file,
        for_signing=res_for_signing,
        shallow_copy=res_shallow_copy,
        start_folder=filter.start_folder,
        use_short_path=filter.use_short_path,
        audit_log=res_audit_log
    )