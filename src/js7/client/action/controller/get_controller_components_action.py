from typing import Any, Dict

from ...context import Context
from ....api.joc.http.v_2_6_5.controller.components import components, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import ControllerIdReq as ControllerIdReq_V_2_6_5


def get_controller_components_action(*, context: Context, controller_id: str) -> Dict[str, Any]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(controller_id)

        result = components(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(controller_id: str) -> ControllerIdReq_V_2_6_5:
    # Validates controller id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Result
    return ControllerIdReq_V_2_6_5(controller_id=controller_id)