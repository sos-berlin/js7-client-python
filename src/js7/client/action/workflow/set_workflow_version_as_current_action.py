from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.workflow.transition import transition, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    ModifyWorkflow as ModifyWorkflow_V_2_6_5,
    WorkflowID as WorkflowID_V_2_6_5
)


def set_workflow_version_as_current_action(
    *, 
    context: Context, 
    controller_id: str,
    workflow_path: str,
    workflow_version_id: str,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            workflow_path=workflow_path,
            workflow_version_id=workflow_version_id,
            audit_log=audit_log
        )

        result = transition(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    workflow_path: str,
    workflow_version_id: str,
    audit_log: Optional[AuditLog]
) -> ModifyWorkflow_V_2_6_5:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required")
    
    # Validate: workflow_version_id
    if not workflow_version_id:
        raise ValueError("'workflow_version_id' is required")
    
    # Validate: workflow_path
    if not workflow_path:
        raise ValueError("'workflow_path' is required")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ModifyWorkflow_V_2_6_5(
        controller_id=controller_id,
        workflow_id=WorkflowID_V_2_6_5(
            path=workflow_path,
            version_id=workflow_version_id
        ),
        audit_log=res_audit_log
    )