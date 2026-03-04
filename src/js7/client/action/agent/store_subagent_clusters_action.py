from typing import List, Optional

from ...context import Context
from ....model.public.client.common.store_agents import SubagentCluster
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    StoreSubagentClusters as StoreSubagentClusters_V_2_8_2,
    SubagentCluster as SubagentCluster_V_2_8_2,
    SubagentID as SubagentID_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_subagent_clusters_action(
    *, 
    context: Context, 
    subagent_clusters: List[SubagentCluster],
    audit_log: Optional[AuditLog]
) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            subagent_clusters=subagent_clusters,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="agents/cluster/store", call=EndpointCall(
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
    subagent_clusters: List[SubagentCluster],
    audit_log: Optional[AuditLog]
) -> StoreSubagentClusters_V_2_8_2:
    
    # Validate: subagent_clusters
    if not subagent_clusters:
        raise ValueError("At least one subagent cluster in 'subagent_clusters' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return StoreSubagentClusters_V_2_8_2(
        subagent_clusters=[
            SubagentCluster_V_2_8_2(
                agent_id=sc.id,
                subagent_cluster_id=sc.subagent_cluster_id,
                title=sc.title,
                subagent_ids=[
                    SubagentID_V_2_8_2(
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