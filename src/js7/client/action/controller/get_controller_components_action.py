from typing import Any, Dict

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    ControllerIdReq as ControllerIdReq_V_2_8_2,
    Components as Components_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def get_controller_components_action(*, context: Context, controller_id: str) -> Dict[str, Any]:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(controller_id)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="controller/components", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, Components_V_2_8_2):
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(controller_id: str) -> ControllerIdReq_V_2_8_2:
    # Validates controller id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Result
    return ControllerIdReq_V_2_8_2(controller_id=controller_id)