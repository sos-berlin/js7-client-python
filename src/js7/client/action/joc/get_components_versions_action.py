from typing import Any, Dict, List, Optional
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    VersionsFilter as VersionsFilter_V_2_8_2,
    VersionResponse as VersionResponse_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_components_versions_action(
    *, 
    context: Context,
    controller_ids: Optional[List[str]],
    agent_ids: Optional[List[str]]
) -> Dict[str, Any]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_ids=controller_ids,
            agent_ids=agent_ids
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="joc/versions", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))
    
    if isinstance(result, VersionResponse_V_2_8_2):
        return result.model_dump(mode="json")

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    controller_ids: Optional[List[str]],
    agent_ids: Optional[List[str]]
) -> VersionsFilter_V_2_8_2:
    
    # Validate: Any of controller_ids or agent_ids
    if not (controller_ids and agent_ids):
        raise ValueError("At least one of 'controller_ids' or 'agent_ids' is required.")
    
    # Result
    return VersionsFilter_V_2_8_2(
        controller_ids=controller_ids,
        agent_ids=agent_ids
    )