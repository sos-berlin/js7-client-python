from typing import List, Optional

from ...context import Context
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.public.client.input.add_order import Order
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.orders.add import add, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AddOrders as AddOrders_V_2_6_5,
    AddOrder as AddOrder_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5,
    PlanID as PlanID_V_2_6_5
)


# Returns: OrderIDs
def add_orders_action(
    *, 
    context: Context,
    controller_id: str,
    orders: List[Order], 
    audit_log: Optional[AuditLog]
) -> List[str]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            timezone=context.client_config.timezone, 
            controller_id=controller_id,
            orders=orders,
            audit_log=audit_log
        )

        result = add(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.order_ids or []
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    timezone: str, 
    controller_id: str,
    orders: List[Order],
    audit_log: Optional[AuditLog]
) -> AddOrders_V_2_6_5:
    
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
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return AddOrders_V_2_6_5(
        controller_id=controller_id,
        audit_log=res_audit_log,
        orders=[
            AddOrder_V_2_6_5(
                arguments=o.arguments,
                block_position=o.block_position,
                end_positions=o.end_positions,
                force_job_admission=o.force_job_admission,
                open_closed_plan=o.open_closed_plan,
                order_name=o.order_name if o.order_name else "unnamed",
                plan_id=(
                    PlanID_V_2_6_5(
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
