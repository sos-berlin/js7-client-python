from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.suspend_order_filter import SuspendOrderFilter
from ....model.private.http.joc.joc_v_2_8_2 import (
    OK as OK_V_2_8_2,
    WorkflowID as WorkflowID_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    SuspendOrders as SuspendOrders_V_2_8_2,
    Folder as Folder_V_2_8_2,
    OrderStateText as OrderStateText_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def suspend_orders_action(*, context: Context, controller_id: str, filter: SuspendOrderFilter, audit_log: Optional[AuditLog]) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id, 
            filter=filter, 
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="orders/suspend", call=EndpointCall(
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
    filter: SuspendOrderFilter, 
    audit_log: Optional[AuditLog]
) -> SuspendOrders_V_2_8_2:
    
    # Build: res_audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: res_workflow_ids
    res_workflow_ids = [
        WorkflowID_V_2_8_2(
            path=id.workflow_path, 
            version_id=id.version_id
        )
        for id in filter.workflow_ids
    ] if filter.workflow_ids else None
    
    # Build: folders
    res_folders = [
        Folder_V_2_8_2(
            folder=folder.folder_path,
            recursive=folder.recursive
        )
        for folder in filter.folders
    ] if filter.folders else None
    
    # Build: States
    res_states = [
        OrderStateText_V_2_8_2(state) # Raises ValueError() if invalid.
        for state in filter.states
    ] if filter.states else None
    
    # Result
    return SuspendOrders_V_2_8_2(
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