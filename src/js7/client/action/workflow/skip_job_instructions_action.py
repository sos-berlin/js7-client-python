from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    OK as OK_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    ModifyWorkflowLabels as ModifyWorkflowLabels_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def skip_job_instructions_action(
    *, 
    context: Context, 
    controller_id: str, 
    workflow_path: str,
    labels: List[str],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id, 
            workflow_path=workflow_path,
            labels=labels,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="workflow/skip", call=EndpointCall(
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
    workflow_path: str,
    labels: List[str],
    audit_log: Optional[AuditLog]
) -> ModifyWorkflowLabels_V_2_8_2:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: workflow_path
    if not workflow_path:
        raise ValueError("'workflow_path' is required.")
    
    # Validate: labels
    if not labels:
        raise ValueError("At least one label in 'labels' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ModifyWorkflowLabels_V_2_8_2(
        controller_id=controller_id,
        workflow_path=workflow_path,
        labels=labels,
        audit_log=res_audit_log
    )