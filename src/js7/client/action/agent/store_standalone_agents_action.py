from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.store_agents import StoreAgent
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    StoreAgents as StoreAgents_V_2_8_2,
    Agent as Agent_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_standalone_agents_action(
    *, 
    context: Context, 
    controller_id: str, 
    agents: List[StoreAgent],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            agents=agents,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="agents/inventory/store", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    controller_id: str, 
    agents: List[StoreAgent],
    audit_log: Optional[AuditLog]
) -> StoreAgents_V_2_8_2:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: agents
    if not agents:
        raise ValueError("At least one agent in 'agents' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return StoreAgents_V_2_8_2(
        controller_id=controller_id,
        agents=[
            Agent_V_2_8_2(
                agent_id=a.id,
                agent_name=a.name,
                agent_name_aliases=a.aliases,
                url=a.url,
                process_limit=a.process_limit,
                hidden=a.hidden
            )
            for a in agents
        ],
        audit_log=res_audit_log
    )