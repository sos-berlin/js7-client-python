from typing import Any, Dict, List

from ...context import Context
from ....model.public.client.filter.tasks_filter import TasksFilter
from ....api.joc.http.v_2_6_5.tasks.history import history, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    JobsFilter as JobsFilter_V_2_6_5,
    Folder as Folder_V_2_6_5,
    HistoryState as HistoryState_V_2_6_5,
    HistoryStateText as HistoryStateText_V_2_6_5,
    JobCriticality as JobCriticality_V_2_6_5
)


def get_task_history_info_action(*, context: Context, controller_id: str, filter: TasksFilter) -> List[Dict[str, Any]]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            timezone=context.client_config.timezone,
            filter=filter
        )

        result = history(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json").get("history") or []
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str,
    timezone: str,
    filter: TasksFilter
) -> JobsFilter_V_2_6_5:
    
    # Validate: controller_id: str
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    return JobsFilter_V_2_6_5(
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
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.folders
        ] if filter.folders else None,
        
        history_states=[
            HistoryState_V_2_6_5(text=HistoryStateText_V_2_6_5(h)) # Raises ValueError() if invalid.
            for h in filter.history_states
        ] if filter.history_states else None,
        
        criticalities=[
            JobCriticality_V_2_6_5(c) # Raises ValueError() if invalid.
            for c in filter.criticalities
        ] if filter.criticalities else None,
        
        exclude_jobs=None,
        history_ids=None,
        jobs=None,
        task_ids=None,
        limit=None,
    )