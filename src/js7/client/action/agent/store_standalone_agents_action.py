from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.store_agents import StoreAgent
from ....api.joc.http.v_2_6_5.agents.inventory.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    StoreAgents as StoreAgents_V_2_6_5,
    Agent as Agent_V_2_6_5
)


def store_standalone_agents_action(
    *, 
    context: Context, 
    controller_id: str, 
    agents: List[StoreAgent],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            agents=agents,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str, 
    agents: List[StoreAgent],
    audit_log: Optional[AuditLog]
) -> StoreAgents_V_2_6_5:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: agents
    if not agents:
        raise ValueError("At least one agent in 'agents' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return StoreAgents_V_2_6_5(
        controller_id=controller_id,
        agents=[
            Agent_V_2_6_5(
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