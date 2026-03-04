from typing import Any, Dict

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.daily_plan_order_filters import DailyPlanProjectionsFilter
from ....model.private.http.joc.joc_v_2_8_2 import (
    Folder as Folder_V_2_8_2,
    ProjectionsRequest as ProjectionsRequest_V_2_8_2,
    ProjectionsCalendarResponse as ProjectionsCalendarResponse_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_projection_dates_action(
    *,
    context: Context,
    filter: DailyPlanProjectionsFilter
) -> Dict[str, Any]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(filter)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/projections/dates", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, ProjectionsCalendarResponse_V_2_8_2):
        return result.model_dump(mode="json").get("years") or {}

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(filter: DailyPlanProjectionsFilter) -> ProjectionsRequest_V_2_8_2:    
    # Result
    return ProjectionsRequest_V_2_8_2(
        date_from=filter.date_from,
        date_to=filter.date_to,
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
        without_start_time=filter.without_start_time,
        controller_ids=filter.controller_ids,
    )
