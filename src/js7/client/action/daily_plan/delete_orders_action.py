from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.daily_plan.orders.delete import delete, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanDeleteOrdersFilter
from ....model.private.http.joc.joc_v_2_6_5 import (
    Folder as Folder_V_2_6_5,
    DailyPlanDeleteOrders as DailyPlanDeleteOrders_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def delete_orders_action(
    *,
    context: Context,
    filter: DailyPlanDeleteOrdersFilter,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            filter=filter,
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
    filter: DailyPlanDeleteOrdersFilter,
    audit_log: Optional[AuditLog],
) -> DailyPlanDeleteOrders_V_2_6_5:
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return DailyPlanDeleteOrders_V_2_6_5(
        daily_plan_date_from=filter.date_from,
        daily_plan_date_to=filter.date_to,
        schedule_paths=filter.schedule_paths,
        schedule_folders=[
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.schedule_folders
        ] if filter.schedule_folders else None,
        workflow_paths=filter.workflow_paths,
        workflow_folders=[
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.workflow_folders
        ] if filter.workflow_folders else None,
        controller_ids=filter.controller_ids,
        order_ids=filter.order_ids,
        late=filter.late,
        submission_history_ids=filter.submission_history_ids,
        audit_log=res_audit_log
    )
