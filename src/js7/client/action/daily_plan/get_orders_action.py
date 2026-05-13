from typing import Any, Dict

from ...context import Context
from ....api.joc.http.v_2_6_5.daily_plan.orders.orders import orders, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanOrdersFilter
from ....model.private.http.joc.joc_v_2_6_5 import (
    DailyPlanOrdersFilter as DailyPlanOrdersFilter_V_2_6_5,
    DailyPlanOrderStateText as DailyPlanOrderStateText_V_2_6_5,
    Folder as Folder_V_2_6_5
)


def get_orders_action(
    *,
    context: Context,
    filter: DailyPlanOrdersFilter,
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(filter)

        result = orders(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(filter: DailyPlanOrdersFilter) -> DailyPlanOrdersFilter_V_2_6_5:    
    # Result
    return DailyPlanOrdersFilter_V_2_6_5(
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
            DailyPlanOrderStateText_V_2_6_5(s) # Returns ValueError() if invalid.
            for s in filter.states
        ] if filter.states else None,
        
        schedule_folders=[
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.schedule_folders
        ] if filter.schedule_folders else None,
        
        workflow_folders=[
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.workflow_folders
        ] if filter.workflow_folders else None
    )
