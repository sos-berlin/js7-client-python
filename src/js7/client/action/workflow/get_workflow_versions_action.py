from typing import Dict
from pathlib import PurePosixPath

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    WorkflowID as WorkflowID_V_2_8_2,
    WorkflowFilter as WorkflowFilter_V_2_8_2,
    Workflow as Workflow_V_2_8_2,
    WorkflowsFilter as WorkflowsFilter_V_2_8_2,
    Workflows as Workflows_V_2_8_2,
    Folder as Folder_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


# Returns: { Version ID: Path }
def get_workflow_versions_action(
    *, 
    context: Context,
    controller_id: str,
    workflow_path: str,
    exclude_current_version: bool,
) -> Dict[str, str]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        result = _build_v_2_8_2_request(
            ctx=context, 
            controller_id=controller_id, 
            workflow_path=workflow_path
        )
        
        return _build_v_2_8_2_response(
            response=result, 
            exclude_current_version=exclude_current_version,
            filter_workflow_path=workflow_path
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    ctx: Context,
    controller_id: str,
    workflow_path: str,
) -> Workflows_V_2_8_2:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: workflow_path
    if not workflow_path:
        raise ValueError("'workflow_path' is required.")
    
    # Request: /workflow
    res_workflow = ctx.joc_api.dispatch(endpoint_id="workflow", call=EndpointCall(
        http_service=ctx.http_service,
        access_token=ctx.auth_provider.login(),
        payload=WorkflowFilter_V_2_8_2(
            controller_id=controller_id,
            workflow_id=WorkflowID_V_2_8_2(
                path=workflow_path,
                version_id=None
            ),
            compact=False
        ),
        options=None,
    ))
    
    if not isinstance(res_workflow, Workflow_V_2_8_2):
        raise RuntimeError(f"Unexpected response type: {type(res_workflow).__name__}")
    
    # Request: /workflows
    if not (res_workflow.workflow and res_workflow.workflow.path):
        raise ValueError("'workflow.path' missing in response.")
    
    res_workflows = ctx.joc_api.dispatch(endpoint_id="workflows", call=EndpointCall(
        http_service=ctx.http_service,
        access_token=ctx.auth_provider.login(),
        payload=WorkflowsFilter_V_2_8_2(
            controller_id=controller_id,
            folders=[Folder_V_2_8_2(
                folder=str(PurePosixPath(res_workflow.workflow.path).parent),
                recursive=False
            )],
            compact=False,
            
        ),
        options=None,
    ))
    
    if not isinstance(res_workflows, Workflows_V_2_8_2):
        raise RuntimeError(f"Unexpected response type: {type(res_workflow).__name__}")
    
    return res_workflows

#----------------------#
# Build 2.8.2 response #
#----------------------#
def _build_v_2_8_2_response(
    *,
    response: Workflows_V_2_8_2,
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
