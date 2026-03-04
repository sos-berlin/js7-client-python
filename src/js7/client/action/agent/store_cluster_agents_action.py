from typing import List, Optional

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.store_agents import StoreClusterAgent
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    StoreClusterAgents as StoreClusterAgents_V_2_8_2,
    ClusterAgent as ClusterAgent_V_2_8_2,
    Subagent as Subagent_V_2_8_2,
    SubagentDirectorType as SubagentDirectorType_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_cluster_agents_action(
    *,
    context: Context, 
    controller_id: str, 
    agents: List[StoreClusterAgent],
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
    result = context.joc_api.dispatch(endpoint_id="agents/inventory/cluster/store", call=EndpointCall(
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
    agents: List[StoreClusterAgent],
    audit_log: Optional[AuditLog]
) -> StoreClusterAgents_V_2_8_2:
    
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validates agents
    if not agents:
        raise ValueError("At least one agent in 'agents' is required.")
    
    # Build: res_audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return StoreClusterAgents_V_2_8_2(
        controller_id=controller_id,
        cluster_agents=[
            ClusterAgent_V_2_8_2(
                agent_id=a.id,
                agent_name=a.name,
                agent_name_aliases=a.aliases,
                title=a.title,
                process_limit=a.process_limit,
                subagents=[
                    Subagent_V_2_8_2(
                        subagent_id=s.id,
                        url=s.url,
                        title=s.title,
                        # Raises ValueError() if invalid.
                        is_director=SubagentDirectorType_V_2_8_2(s.director_type) if s.director_type else None, 
                        ordering=s.order,
                        with_generate_subagent_cluster=s.with_generate_subagent_cluster
                    )
                    for s in a.subagents
                ]
            )
            for a in agents
        ],
        audit_log=res_audit_log
    )