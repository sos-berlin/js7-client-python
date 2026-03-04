from typing import List, Optional, Tuple

from ...context import Context
from ....model.public.client.common.cycle import Cycle
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    DailyPlanCopyOrder as DailyPlanCopyOrder_V_2_8_2,
    Cycle as Cycle_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    OrderIDMap200 as OrderIDMap200_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def copy_orders_action(
    *,
    context: Context,
    controller_id: str,
    order_ids: List[str],
    scheduled_for: Optional[ScheduleTime],
    cycle: Optional[Cycle],
    force_job_admission: bool,
    sticky_daily_plan_date: bool,
    audit_log: Optional[AuditLog]
) -> List[Tuple[str, str]]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            timezone=context.client_config.timezone,
            controller_id=controller_id,
            order_ids=order_ids,
            scheduled_for=scheduled_for,
            cycle=cycle,
            force_job_admission=force_job_admission,
            sticky_daily_plan_date=sticky_daily_plan_date,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/orders/copy", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, OrderIDMap200_V_2_8_2):
        return [
            (old_id, new_id)
            for old_id, new_id in result.order_ids
        ] if result.order_ids else []

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    timezone: str,
    controller_id: str,
    order_ids: List[str],
    scheduled_for: Optional[ScheduleTime],
    cycle: Optional[Cycle],
    force_job_admission: bool,
    sticky_daily_plan_date: bool,
    audit_log: Optional[AuditLog]
) -> DailyPlanCopyOrder_V_2_8_2:    
    
    # Validate: timezone
    if not timezone:
        raise ValueError("'timezone' is required in client config.")
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: order_ids
    if not order_ids:
        raise ValueError("At least one order id in 'order_ids' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return DailyPlanCopyOrder_V_2_8_2(
        time_zone=timezone,
        controller_id=controller_id,
        order_ids=order_ids,
        scheduled_for=scheduled_for.value if scheduled_for else None,
        cycle=Cycle_V_2_8_2(
            begin=str(cycle.begin),
            end=str(cycle.end),
            repeat=str(cycle.repeat)
        ) if cycle else None,
        force_job_admission=force_job_admission,
        stick_daily_plan_date=sticky_daily_plan_date,
        audit_log=res_audit_log
    )
