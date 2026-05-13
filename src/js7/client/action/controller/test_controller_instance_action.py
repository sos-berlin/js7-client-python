from typing import Optional

from ...context import Context
from ....api.joc.http.v_2_6_5.controller.test import test, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    TestConnect as TestConnect_V_2_6_5,
    ConnectionStateText as ConnectionStateText_V_2_6_5
)


def test_controller_instance_action(
    *, 
    context: Context, 
    controller_id: Optional[str], 
    url: str
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            url=url
        )

        result = test(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        if (
            result.controller
            and result.controller.connection_state
            and result.controller.connection_state.text == ConnectionStateText_V_2_6_5.ESTABLISHED
        ):
            return True

        return False
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: Optional[str], 
    url: str
) -> TestConnect_V_2_6_5:

    # Validates controller id
    if not url:
        raise ValueError("'url' is required.")

    # Result
    return TestConnect_V_2_6_5(
        controller_id=controller_id,
        url=url
    )