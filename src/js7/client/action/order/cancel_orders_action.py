from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.orders.cancel import cancel, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    CancelOrders as CancelOrders_V_2_6_5,
    WorkflowID as WorkflowID_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def cancel_orders_action(
    *, 
    context: Context, 
    controller_id: str, 
    order_ids: Optional[List[str]], 
    workflow_paths: Optional[List[str]],
    kill: bool,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            timezone=context.client_config.timezone,
            order_ids=order_ids, 
            workflow_paths=workflow_paths,
            kill=kill,
            audit_log=audit_log
        )

        result = cancel(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str, 
    timezone: str,
    order_ids: Optional[List[str]], 
    workflow_paths: Optional[List[str]],
    kill: bool,
    audit_log: Optional[AuditLog]
) -> CancelOrders_V_2_6_5:
    
    # Validate: timezone
    if not timezone:
        raise ValueError("'timezone' is required in client configuration.")
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: Any of order_ids or workflow_paths
    if not (order_ids or workflow_paths):
        raise ValueError("At least one of 'order_ids' or 'workflow_paths' must be provided.")
    
    # Build: res_audit_log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: res_workflow_ids
    res_workflow_ids = [
        WorkflowID_V_2_6_5(path=path)
        for path in workflow_paths
    ] if workflow_paths else None
    
    # Result
    return CancelOrders_V_2_6_5(
        controller_id=controller_id,
        workflow_ids=res_workflow_ids,
        order_ids=order_ids,
        audit_log=res_audit_log,
        kill=kill,
        time_zone=timezone
    )