from pathlib import Path
from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import DraftConfiguration, DeployConfiguration
from ....model.public.client.filter.export_filter import ExportFilter
from ....api.joc.http.v_2_6_5.inventory.export.export import export, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    PublishConfiguration as Configuration_V_2_6_5,
    ExportFilter as ExportFilter_V_2_6_5,
    ExportForSigning as ExportForSigning_V_2_6_5,
    DeployablesValidFilter as DeployablesValidFilter_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    Config as Config_V_2_6_5,
    ExportFile as ExportFile_V_2_6_5,
    ArchiveFormat as ArchiveFormat_V_2_6_5,
    ExportShallowCopy as ExportShallowCopy_V_2_6_5,
    DeployablesFilter as DeployablesFilter_V_2_6_5,
    ReleasablesFilter as ReleasablesFilter_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)

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
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        # Normalize out_path
        out_dir = Path(out_dir)
    
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            out_dir=out_dir,
            filename=filename,
            archive_format=archive_format,
            filter=filter,
            audit_log=audit_log
        )

        result = export(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bytes_to_file(data=result, out_path=Path(out_dir / filename))
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    out_dir: Path,
    filename: str,
    archive_format: Literal["ZIP", "TAR_GZ"],
    filter: ExportFilter,
    audit_log: Optional[AuditLog]
) -> ExportFilter_V_2_6_5:
    
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
    res_export_file = ExportFile_V_2_6_5(
        filename=Path(out_dir / filename).name,
        format=(ArchiveFormat_V_2_6_5(archive_format)) # Raises ValueError() if invalid.
    )
    
    # Build: configurations
    res_draft_configurations: Optional[List[Config_V_2_6_5]] = None
    res_deploy_configurations: Optional[List[Config_V_2_6_5]] = None
    res_release_configurations: Optional[List[Config_V_2_6_5]] = None
    for config in filter.configurations:
        if isinstance(config, DraftConfiguration):
            if not res_draft_configurations:
                res_draft_configurations = []
            
            res_draft_configurations.append(
                Config_V_2_6_5(
                    configuration=Configuration_V_2_6_5(
                        object_type=ConfigurationType_V_2_6_5(config.object_type), # Raises ValueError() if invalid.
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
                Config_V_2_6_5(
                    configuration=Configuration_V_2_6_5(
                        commit_id=config.commit_id,
                        object_type=ConfigurationType_V_2_6_5(config.object_type), # Raises ValueError() if invalid.
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
                Config_V_2_6_5(
                    configuration=Configuration_V_2_6_5(
                        object_type=ConfigurationType_V_2_6_5(config.object_type), # Raises ValueError() if invalid.
                        path=config.path,
                        recursive=config.recursive
                    )
                )
            )
    
    # Build: for_signing
    res_for_signing = ExportForSigning_V_2_6_5(
        controller_id=controller_id,
        deployables=DeployablesValidFilter_V_2_6_5(
            deploy_configurations=res_deploy_configurations,
            draft_configurations=res_draft_configurations
        )
    ) if filter.for_signing is True else None
        
    # Build: shallow_copy
    res_shallow_copy = ExportShallowCopy_V_2_6_5(
        incl_all_tags=filter.include_all_tags,
        deployables=DeployablesFilter_V_2_6_5(
            without_invalid=filter.without_invalid_drafts,
            draft_configurations=res_draft_configurations,
            deploy_configurations=res_deploy_configurations
        ),
        releasables=ReleasablesFilter_V_2_6_5(
            without_invalid=filter.without_invalid_drafts,
            draft_configurations=res_draft_configurations,
            released_configurations=res_release_configurations
        ) if (res_draft_configurations or res_release_configurations) else None
    ) if filter.for_signing is False else None

    # Build: audit_log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ExportFilter_V_2_6_5(
        export_file=res_export_file,
        for_signing=res_for_signing,
        shallow_copy=res_shallow_copy,
        start_folder=filter.start_folder,
        use_short_path=filter.use_short_path,
        audit_log=res_audit_log
    )