from typing import Any, Dict

from ...context import Context
from ....model.public.client.filter.tasks_filter import TasksFilter
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    JobsFilter as JobsFilter_V_2_8_2,
    TaskHistory as TaskHistory_V_2_8_2,
    Folder as Folder_V_2_8_2,
    HistoryState as HistoryState_V_2_8_2,
    HistoryStateText as HistoryStateText_V_2_8_2,
    JobCriticality as JobCriticality_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_task_history_info_action(*, context: Context, controller_id: str, filter: TasksFilter) -> Dict[str, Any]:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            timezone=context.client_config.timezone,
            filter=filter
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="tasks/history", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, TaskHistory_V_2_8_2):
        return result.model_dump(mode="json").get("history") or {}
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    controller_id: str,
    timezone: str,
    filter: TasksFilter
) -> JobsFilter_V_2_8_2:
    
    # Validate: controller_id: str
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    return JobsFilter_V_2_8_2(
        controller_id=controller_id,
        time_zone=timezone,
        
        date_from=filter.date_from.isoformat() if filter.date_from else None,
        date_to=filter.date_to.isoformat() if filter.date_to else None,
        completed_date_from=filter.completed_date_from.isoformat() if filter.completed_date_from else None,
        completed_date_to=filter.completed_date_to.isoformat() if filter.completed_date_to else None,
        
        job_name=filter.job_name,
        workflow_name=filter.workflow_name,
        workflow_path=filter.workflow_paths,
        
        folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.folders
        ] if filter.folders else None,
        
        history_states=[
            HistoryState_V_2_8_2(text=HistoryStateText_V_2_8_2(h)) # Raises ValueError() if invalid.
            for h in filter.history_states
        ] if filter.history_states else None,
        
        criticalities=[
            JobCriticality_V_2_8_2(c) # Raises ValueError() if invalid.
            for c in filter.criticalities
        ] if filter.criticalities else None,
        
        exclude_jobs=None,
        history_ids=None,
        jobs=None,
        task_ids=None,
        limit=None,
    )