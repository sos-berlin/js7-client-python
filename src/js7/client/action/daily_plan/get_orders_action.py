from typing import Any, Dict

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanOrdersFilter
from ....model.private.http.joc.joc_v_2_8_2 import (
    DailyPlanOrdersFilter as DailyPlanOrdersFilter_V_2_8_2,
    PlannedOrders as PlannedOrders_V_2_8_2,
    DailyPlanOrderStateText as DailyPlanOrderStateText_V_2_8_2,
    Folder as Folder_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_orders_action(
    *,
    context: Context,
    filter: DailyPlanOrdersFilter,
) -> Dict[str, Any]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(filter)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/orders", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, PlannedOrders_V_2_8_2):
        return result.model_dump(mode="json")

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(filter: DailyPlanOrdersFilter) -> DailyPlanOrdersFilter_V_2_8_2:    
    # Result
    return DailyPlanOrdersFilter_V_2_8_2(
        daily_plan_date_from=filter.date_from,
        daily_plan_date_to=filter.date_to,
        controller_ids=filter.controller_ids,
        late=filter.late,
        order_ids=filter.order_ids,
        order_tags=filter.order_tags,
        workflow_tags=filter.workflow_tags,
        workflow_paths=filter.workflow_paths,
        schedule_paths=filter.schedule_paths,
        
        states=[
            DailyPlanOrderStateText_V_2_8_2(s) # Returns ValueError() if invalid.
            for s in filter.states
        ] if filter.states else None,
        
        schedule_folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.schedule_folders
        ] if filter.schedule_folders else None,
        
        workflow_folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.workflow_folders
        ] if filter.workflow_folders else None
    )
