from typing import Any, Dict, List

from ...context import Context
from ....api.joc.http.v_2_6_5.agents.agents import agents, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    ReadAgentsV as ReadAgentsV_V_2_6_5,
)


def get_agents_status_action(
    *, 
    context: Context, 
    controller_id: str, 
    agent_ids: List[str]
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            agent_ids=agent_ids
        )

        result = agents(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json").get("agents") or {}
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, controller_id: str, agent_ids: List[str]) -> ReadAgentsV_V_2_6_5:
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: agent_ids
    if not agent_ids:
        raise ValueError("At least one agent id in 'agent_ids' is required.")
    
    # Result
    return ReadAgentsV_V_2_6_5(
        controller_id=controller_id,
        agent_ids=agent_ids,
        compact=False,
    )