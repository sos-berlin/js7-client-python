from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanDeleteOrdersFilter
from ....model.private.http.joc.joc_v_2_8_2 import (
    Folder as Folder_V_2_8_2,
    DailyPlanDeleteOrders as DailyPlanDeleteOrders_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def delete_orders_action(
    *,
    context: Context,
    filter: DailyPlanDeleteOrdersFilter,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            filter=filter,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/orders/delete", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    filter: DailyPlanDeleteOrdersFilter,
    audit_log: Optional[AuditLog],
) -> DailyPlanDeleteOrders_V_2_8_2:
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return DailyPlanDeleteOrders_V_2_8_2(
        daily_plan_date_from=filter.date_from,
        daily_plan_date_to=filter.date_to,
        schedule_paths=filter.schedule_paths,
        schedule_folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.schedule_folders
        ] if filter.schedule_folders else None,
        workflow_paths=filter.workflow_paths,
        workflow_folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.workflow_folders
        ] if filter.workflow_folders else None,
        controller_ids=filter.controller_ids,
        order_ids=filter.order_ids,
        late=filter.late,
        submission_history_ids=filter.submission_history_ids,
        audit_log=res_audit_log
    )
