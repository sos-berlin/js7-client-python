from typing import Any, Dict, List

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    ReadAgentsV as ReadAgentsV_V_2_8_2,
    AgentsV as AgentsV_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_agents_status_action(
    *, 
    context: Context, 
    controller_id: str, 
    agent_ids: List[str]
) -> Dict[str, Any]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(controller_id=controller_id, agent_ids=agent_ids)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="agents", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, AgentsV_V_2_8_2):
        return result.model_dump(mode="json").get("agents") or {}
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, controller_id: str, agent_ids: List[str]) -> ReadAgentsV_V_2_8_2:
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: agent_ids
    if not agent_ids:
        raise ValueError("At least one agent id in 'agent_ids' is required.")
    
    # Result
    return ReadAgentsV_V_2_8_2(
        controller_id=controller_id,
        agent_ids=agent_ids,
        compact=False,
    )