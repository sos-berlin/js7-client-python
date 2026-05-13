from typing import Optional, List

from ...context import Context
from ....api.joc.http.v_2_6_5.agents.inventory.cluster.subagents.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.store_agents import StoreSubagent
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    StoreSubAgents as StoreSubAgents_V_2_6_5,
    Subagent as Subagent_V_2_6_5,
    SubagentDirectorType as SubagentDirectorType_V_2_6_5
)


def store_subagents_action(
    *, 
    context: Context, 
    controller_id: str,
    agent_id: str,
    subagents: List[StoreSubagent],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            agent_id=agent_id,
            subagents=subagents,
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
    agent_id: str,
    subagents: List[StoreSubagent],
    audit_log: Optional[AuditLog]
) -> StoreSubAgents_V_2_6_5:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: agent_id
    if not agent_id:
        raise ValueError("'agent_id' is required.")
    
    # Validate: subagents
    if not subagents:
        raise ValueError("At least one subagent in 'subagents' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return StoreSubAgents_V_2_6_5(
        controller_id=controller_id,
        agent_id=agent_id,
        subagents=[
            Subagent_V_2_6_5(
                subagent_id=s.id,
                url=s.url,
                title=s.title,
                # Raises ValueError() if invalid
                is_director=SubagentDirectorType_V_2_6_5(s.director_type) if s.director_type else None,
                with_generate_subagent_cluster=s.with_generate_subagent_cluster,
                ordering=s.order
            )
            for s in subagents
        ],
        audit_log=res_audit_log
    )