from pathlib import Path
from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    AgentExportFilter as AgentExportFilter_V_2_8_2,
    ExportFile as ExportFile_V_2_8_2,
    ArchiveFormat as ArchiveFormat_V_2_8_2
)

from ....util.bytes_converter.bytes_to_file import bytes_to_file
from ....util.check_matching_version import check_matching_version


def export_agents_action(
    *, 
    context: Context, 
    out_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    agent_ids: List[str],
    audit_log: Optional[AuditLog]
) -> bool:
    
    # Normalize out_path
    out_path = Path(out_path)

    # Determine expected suffix from archive_format
    expected_suffix = ".tar.gz" if archive_format == "TAR_GZ" else ".zip"

    # Append suffix if missing or wrong
    if not out_path.name.endswith((".zip", ".tar.gz")):
        out_path = out_path.with_name(out_path.name + expected_suffix)

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            out_path=out_path,
            archive_format=archive_format,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="agents/export", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, bytes):
        return bytes_to_file(data=result, out_path=Path(out_path))
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    out_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    agent_ids: List[str],
    audit_log: Optional[AuditLog]
) -> AgentExportFilter_V_2_8_2:
    
    # Validate: out_path
    if not out_path:
        raise ValueError("'out_path' is required.")
    
    # Validate: archive_format
    if not archive_format:
        raise ValueError("'archive_format' is required.")
    
    # Validate: agent_ids
    if not agent_ids:
        raise ValueError("At least one agent id in 'agent_ids' is required.")
    
    # Build: export_file
    res_export_file = ExportFile_V_2_8_2(
        filename=Path(out_path).name,
        format=(ArchiveFormat_V_2_8_2(archive_format)) # Raises ValueError() if invalid.
    )
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return AgentExportFilter_V_2_8_2(
        agent_ids=agent_ids,
        export_file=res_export_file,
        audit_log=res_audit_log
    )