from typing import Any, Dict

from ...context import Context
from ....api.joc.http.v_2_6_5.daily_plan.projections.calendar import calendar, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanProjectionsFilter
from ....model.private.http.joc.joc_v_2_6_5 import (
    Folder as Folder_V_2_6_5,
    ProjectionsRequest as ProjectionsRequest_V_2_6_5
)


def get_calendar_projections_action(
    *,
    context: Context,
    filter: DailyPlanProjectionsFilter
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(filter)

        result = calendar(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json").get("years") or {}
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(filter: DailyPlanProjectionsFilter) -> ProjectionsRequest_V_2_6_5:    
    # Result
    return ProjectionsRequest_V_2_6_5(
        date_from=filter.date_from,
        date_to=filter.date_to,
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
        without_start_time=filter.without_start_time,
        controller_ids=filter.controller_ids,
    )
