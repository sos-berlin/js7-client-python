from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.orders.suspend import suspend, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.filter.suspend_order_filter import SuspendOrderFilter
from ....model.private.http.joc.joc_v_2_6_5 import (
    WorkflowID as WorkflowID_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5,
    SuspendOrders as SuspendOrders_V_2_6_5,
    Folder as Folder_V_2_6_5,
    OrderStateText as OrderStateText_V_2_6_5
)


def suspend_orders_action(*, context: Context, controller_id: str, filter: SuspendOrderFilter, audit_log: Optional[AuditLog]) -> bool:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            filter=filter, 
            audit_log=audit_log
        )

        result = suspend(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str, 
    filter: SuspendOrderFilter, 
    audit_log: Optional[AuditLog]
) -> SuspendOrders_V_2_6_5:
    
    # Build: res_audit_log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: res_workflow_ids
    res_workflow_ids = [
        WorkflowID_V_2_6_5(
            path=id.workflow_path, 
            version_id=id.version_id
        )
        for id in filter.workflow_ids
    ] if filter.workflow_ids else None
    
    # Build: folders
    res_folders = [
        Folder_V_2_6_5(
            folder=folder.folder_path,
            recursive=folder.recursive
        )
        for folder in filter.folders
    ] if filter.folders else None
    
    # Build: States
    res_states = [
        OrderStateText_V_2_6_5(state) # Raises ValueError() if invalid.
        for state in filter.states
    ] if filter.states else None
    
    # Result
    return SuspendOrders_V_2_6_5(
        controller_id=controller_id,
        order_ids=filter.order_ids,
        workflow_ids=res_workflow_ids,
        folders=res_folders,
        states=res_states,
        date_from=filter.date_from,
        date_to=filter.date_to,
        time_zone=filter.timezone,
        reset=filter.reset,
        kill=filter.kill,
        deep=filter.deep,
        audit_log=res_audit_log
    )