from typing import Dict
from pathlib import PurePosixPath

from ...context import Context
from ....api.joc.http.v_2_6_5.workflow.workflow import workflow, EndpointCall as WorkflowEndpointCall
from ....api.joc.http.v_2_6_5.workflows.workflows import workflows, EndpointCall as WorkflowsEndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    WorkflowID as WorkflowID_V_2_6_5,
    WorkflowFilter as WorkflowFilter_V_2_6_5,
    WorkflowsFilter as WorkflowsFilter_V_2_6_5,
    Workflows as Workflows_V_2_6_5,
    Folder as Folder_V_2_6_5
)


# Returns: { Version ID: Path }
def get_workflow_versions_action(
    *, 
    context: Context,
    controller_id: str,
    workflow_path: str,
    exclude_current_version: bool,
) -> Dict[str, str]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = _build_v_2_6_5_request(
            ctx=context, 
            controller_id=controller_id, 
            workflow_path=workflow_path
        )
        
        return _build_v_2_6_5_response(
            response=result, 
            exclude_current_version=exclude_current_version,
            filter_workflow_path=workflow_path
        )
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    ctx: Context,
    controller_id: str,
    workflow_path: str,
) -> Workflows_V_2_6_5:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: workflow_path
    if not workflow_path:
        raise ValueError("'workflow_path' is required.")
    
    res_workflow = workflow(WorkflowEndpointCall(
        http_service=ctx.http_service,
        access_token=ctx.auth_provider.login(),
        payload=WorkflowFilter_V_2_6_5(
            controller_id=controller_id,
            workflow_id=WorkflowID_V_2_6_5(
                path=workflow_path,
                version_id=None
            ),
            compact=False
        )
    ))
    
    # Request: /workflows
    if not (res_workflow.workflow and res_workflow.workflow.path):
        raise ValueError("'workflow.path' missing in response.")
    
    res_workflows = workflows(WorkflowsEndpointCall(
        http_service=ctx.http_service,
        access_token=ctx.auth_provider.login(),
        payload=WorkflowsFilter_V_2_6_5(
            controller_id=controller_id,
            folders=[Folder_V_2_6_5(
                folder=str(PurePosixPath(res_workflow.workflow.path).parent),
                recursive=False
            )],
            compact=False,
            
        )
    ))
    
    return res_workflows

def _build_v_2_6_5_response(
    *,
    response: Workflows_V_2_6_5,
    exclude_current_version: bool,
    filter_workflow_path: str
) -> Dict[str, str]:
    res: Dict[str, str] = {}
    
    # Returns empty dictionary if no workflows found
    if not response.workflows:
        return res
    
    for w in response.workflows:
        # Remove: Not matching workflows paths
        if w.path != filter_workflow_path:
            continue
        
        # Filter: exclude_current_version
        if exclude_current_version and w.is_current_version:
            continue
    
        if not (w.version_id and w.path):
            continue
        
        res[w.version_id] = w.path

    return res
