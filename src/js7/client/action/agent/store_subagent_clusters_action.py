from typing import List, Optional

from ...context import Context
from ....model.public.client.common.store_agents import SubagentCluster
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.agents.cluster.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    StoreSubagentClusters as StoreSubagentClusters_V_2_6_5,
    SubagentCluster as SubagentCluster_V_2_6_5,
    SubagentID as SubagentID_V_2_6_5
)


def store_subagent_clusters_action(
    *, 
    context: Context, 
    subagent_clusters: List[SubagentCluster],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            subagent_clusters=subagent_clusters,
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
    subagent_clusters: List[SubagentCluster],
    audit_log: Optional[AuditLog]
) -> StoreSubagentClusters_V_2_6_5:
    
    # Validate: subagent_clusters
    if not subagent_clusters:
        raise ValueError("At least one subagent cluster in 'subagent_clusters' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return StoreSubagentClusters_V_2_6_5(
        subagent_clusters=[
            SubagentCluster_V_2_6_5(
                agent_id=sc.id,
                subagent_cluster_id=sc.subagent_cluster_id,
                title=sc.title,
                subagent_ids=[
                    SubagentID_V_2_6_5(
                        subagent_id=id,
                        priority=priority
                    )
                    for id, priority in sc.subagent_ids
                ] if sc.subagent_ids else None,
            )
            for sc in subagent_clusters
        ],
        audit_log=res_audit_log
    )