from pathlib import Path
from typing import List, Literal, Union

from ...context import Context
from ....api.joc.http.v_2_6_5.agents.export import export, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AgentExportFilter as AgentExportFilter_V_2_6_5,
    ExportFile as ExportFile_V_2_6_5,
    ArchiveFormat as ArchiveFormat_V_2_6_5
)

from ....util.bytes_converter.bytes_to_file import bytes_to_file


def export_agents_action(
    *, 
    context: Context, 
    out_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    agent_ids: List[str]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        # Normalize out_path
        out_path = Path(out_path)

        # Determine expected suffix from archive_format
        expected_suffix = ".tar.gz" if archive_format == "TAR_GZ" else ".zip"

        # Append suffix if missing or wrong
        if not out_path.name.endswith((".zip", ".tar.gz")):
            out_path = out_path.with_name(out_path.name + expected_suffix)
        
        request_data = _build_v_2_6_5_request(
            out_path=out_path,
            archive_format=archive_format,
            agent_ids=agent_ids
        )

        result = export(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bytes_to_file(data=result, out_path=out_path)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")


def _build_v_2_6_5_request(
    *,
    out_path: Union[Path, str],
    archive_format: Literal["ZIP", "TAR_GZ"],
    agent_ids: List[str]
) -> AgentExportFilter_V_2_6_5:
    
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
    res_export_file = ExportFile_V_2_6_5(
        filename=Path(out_path).name,
        format=(ArchiveFormat_V_2_6_5(archive_format)) # Raises ValueError() if invalid.
    )

    # Result
    return AgentExportFilter_V_2_6_5(
        agent_ids=agent_ids,
        export_file=res_export_file
    )