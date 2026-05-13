from typing import Any, Dict, List, Optional
from ...context import Context
from ....api.joc.http.v_2_6_5.joc.versions import versions, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    VersionsFilter as VersionsFilter_V_2_6_5
)


def get_components_versions_action(
    *, 
    context: Context,
    controller_ids: Optional[List[str]],
    agent_ids: Optional[List[str]]
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_ids=controller_ids,
            agent_ids=agent_ids
        )

        result = versions(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_ids: Optional[List[str]],
    agent_ids: Optional[List[str]]
) -> VersionsFilter_V_2_6_5:
    
    # Validate: Any of controller_ids or agent_ids
    if not (controller_ids or agent_ids):
        raise ValueError("At least one of 'controller_ids' or 'agent_ids' is required.")
    
    # Result
    return VersionsFilter_V_2_6_5(
        controller_ids=controller_ids,
        agent_ids=agent_ids
    )