from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.agents.inventory.cluster.subagents.reset import reset, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    SubAgentCommand as SubAgentCommand_V_2_6_5
)


def reset_subagent_action(
    *, 
    context: Context, 
    controller_id: str,
    subagent_id: str,
    force: bool,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            subagent_id=subagent_id,
            force=force,
            audit_log=audit_log
        )

        result = reset(EndpointCall(
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
    force: bool,
    audit_log: Optional[AuditLog]
) -> SubAgentCommand_V_2_6_5:
    
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validates subagent_id
    if not subagent_id:
        raise ValueError("At least one agent id in 'subagent_id' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return SubAgentCommand_V_2_6_5(
        controller_id=controller_id,
        subagent_id=subagent_id,
        force=force,
        audit_log=res_audit_log
    )