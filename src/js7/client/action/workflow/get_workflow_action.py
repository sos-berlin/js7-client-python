from typing import Dict, Any

from ...context import Context
from ....api.joc.http.v_2_6_5.workflow.workflow import workflow, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    WorkflowFilter as WorkflowFilter_V_2_6_5,
    WorkflowID as WorkflowID_V_2_6_5
)


def get_workflow_action(
    *, 
    context: Context, 
    controller_id: str, 
    workflow_path: str,
    compact: bool
) -> Dict[str, Any]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            workflow_path=workflow_path, 
            compact=compact
        )

        result = workflow(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json").get("workflow") or {}
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str, 
    workflow_path: str,
    compact: bool
) -> WorkflowFilter_V_2_6_5:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: workflow_path
    if not workflow_path:
        raise ValueError("'workflow_path' is required.")
    
    # Result
    return WorkflowFilter_V_2_6_5(
        controller_id=controller_id,
        workflow_id=WorkflowID_V_2_6_5(
            path=workflow_path
        ),
        compact=compact
    )
