from typing import List

from ...context import Context
from ....api.joc.http.v_2_6_5.workflows.search import search as api_search, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    WorkflowSearchFilter as WorkflowSearchFilter_V_2_6_5,
)


# Returns: [Workflow Paths]
def search_workflows_action(*, context: Context, controller_id: str, search: str) -> List[str]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id, 
            search=search
        )

        result = api_search(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        wf_paths: List[str] = []
        
        if result.results:
            for r in result.results:
                if r.path:
                    wf_paths.append(r.path)
        
        return wf_paths
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")


def _build_v_2_6_5_request(*, controller_id: str, search: str) -> WorkflowSearchFilter_V_2_6_5:
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: search
    if not search:
        raise ValueError("'search' is required.")
    
    return WorkflowSearchFilter_V_2_6_5(
        controller_id=controller_id,
        search=search
    )
