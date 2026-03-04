from typing import List

from ...context import Context
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.get_order_filter import GetOrderFilter
from ....model.public.client.input.add_order import Order, PlanID
from ....model.private.http.joc.joc_v_2_8_2 import (
    OrdersFilterV as OrdersFilterV_V_2_8_2,
    OrderStateText as OrderStateText_V_2_8_2,
    OrdersV as OrdersV_V_2_8_2
)

from ....util.check_matching_version import check_matching_version
from ....util.str_converter.order_id_to_order_name import order_id_to_order_name


def get_orders_action(*, context: Context, controller_id: str, filter: GetOrderFilter) -> List[Order]:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(controller_id=controller_id, filter=filter)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="orders", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OrdersV_V_2_8_2):
        return [
            Order(
                arguments=o.arguments,
                block_position=o.position,
                end_positions=o.end_positions,
                force_job_admission=False,
                open_closed_plan=False,
                order_name = order_id_to_order_name(o.order_id),
                plan_id=PlanID(
                    notice_space_key=o.plan_id.notice_space_key,
                    plan_schema_id=o.plan_id.plan_schema_id
                ) if o.plan_id else None,
                priority=o.priority,
                scheduled_for=ScheduleTime.normalize(o.scheduled_for),
                start_position=None,
                tags=o.tags,
                workflow_path=o.workflow_id.path or "" if o.workflow_id else ""
            )
            for o in result.orders
        ] if result.orders else []
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, controller_id: str, filter: GetOrderFilter) -> OrdersFilterV_V_2_8_2:
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Build: States
    res_states = [
        OrderStateText_V_2_8_2(state) # Raises ValueError() if invalid.
        for state in filter.states
    ] if filter.states else None
    
    # Result
    return OrdersFilterV_V_2_8_2(
        controller_id=controller_id,
        compact=filter.compact,
        limit=filter.limit,
        order_ids=filter.order_ids,
        order_tags=filter.order_tags,
        regex=filter.regex,
        state_date_from=filter.state_date_from,
        state_date_to=filter.state_date_to,
        states=res_states,
        without_workflow_tags=filter.without_workflow_tags,
        workflow_tags=filter.workflow_tags
    )
