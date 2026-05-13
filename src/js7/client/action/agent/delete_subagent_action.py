from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....util.version_to_tuple import version_to_tuple
from ....api.joc.http.v_2_6_5.agents.inventory.cluster.subagents.delete import delete, EndpointCall
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    SubAgentsCommand as SubAgentsCommand_V_2_6_5
)


def delete_subagent_action(
    *, 
    context: Context, 
    controller_id: str, 
    subagent_id: str,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            subagent_id=subagent_id,
            audit_log=audit_log
        )

        result = delete(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    subagent_id: str,
    audit_log: Optional[AuditLog]
) -> SubAgentsCommand_V_2_6_5:
    
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validates subagent_id
    if not subagent_id:
        raise ValueError("'subagent_id' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return SubAgentsCommand_V_2_6_5(
        controller_id=controller_id,
        subagent_ids=[
            subagent_id
        ],
        audit_log=res_audit_log
    )