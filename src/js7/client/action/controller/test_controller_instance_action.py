from typing import Optional

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    TestConnect as TestConnect_V_2_8_2,
    JobScheduler200 as JobScheduler200_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def test_controller_instance_action(
    *, 
    context: Context, 
    controller_id: Optional[str], 
    url: str
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            url=url
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="controller/test", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))

    if isinstance(result, JobScheduler200_V_2_8_2):
        if not (
            result.controller
            and result.controller.connection_state 
            and result.controller.connection_state.severity != 0
        ):
            return False
        
        return True
                
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    controller_id: Optional[str], 
    url: str
) -> TestConnect_V_2_8_2:

    # Validates controller id
    if not url:
        raise ValueError("'url' is required.")

    # Result
    return TestConnect_V_2_8_2(
        controller_id=controller_id,
        url=url
    )