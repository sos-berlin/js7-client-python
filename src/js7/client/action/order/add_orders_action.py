from typing import List, Optional

from ...context import Context
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.public.client.input.add_order import Order
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AddOrders as AddOrders_V_2_8_2,
    AddOrder as AddOrder_V_2_8_2,
    OrderIDS as OrderIDS_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    PlanID as PlanID_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


# Returns: OrderIDs
def add_orders_action(
    *, 
    context: Context,
    controller_id: str,
    orders: List[Order], 
    audit_log: Optional[AuditLog]
) -> List[str]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            timezone=context.client_config.timezone, 
            controller_id=controller_id,
            orders=orders,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="orders/add", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OrderIDS_V_2_8_2):
        if not result.order_ids:
            raise RuntimeError("No order id returned by server.")
        return result.order_ids
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    timezone: str, 
    controller_id: str,
    orders: List[Order],
    audit_log: Optional[AuditLog]
) -> AddOrders_V_2_8_2:
    
    # Validate: timezone
    if not timezone:
        raise ValueError("'timezone' is required in client configuration.")
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: orders
    if not orders:
        raise ValueError("At least one order in 'orders' is required.")
    
    # Build: audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return AddOrders_V_2_8_2(
        controller_id=controller_id,
        audit_log=res_audit_log,
        orders=[
            AddOrder_V_2_8_2(
                arguments=o.arguments,
                block_position=o.block_position,
                end_positions=o.end_positions,
                force_job_admission=o.force_job_admission,
                open_closed_plan=o.open_closed_plan,
                order_name=o.order_name if o.order_name else "unnamed",
                plan_id=(
                    PlanID_V_2_8_2(
                        notice_space_key=o.plan_id.notice_space_key, 
                        plan_schema_id=o.plan_id.plan_schema_id
                    )
                    if o.plan_id else None
                ),
                priority=o.priority,
                scheduled_for=(
                    o.scheduled_for.value 
                    if o.scheduled_for 
                    else None
                ) if isinstance(o.scheduled_for, ScheduleTime) else o.scheduled_for,
                start_position=o.start_position,
                tags=o.tags,
                time_zone=timezone,
                workflow_path=o.workflow_path,
            )
            for o in orders
        ]
    )
