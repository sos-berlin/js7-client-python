from typing import Any, Dict, Tuple

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    Js7LicenseInfo as Js7LicenseInfo_V_2_8_2
)


def get_license_info_action(*, context: Context) -> Tuple[bool, Dict[str, Any]]:
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="joc/license", call=EndpointCall(
        http_service=context.http_service,
        payload=None,
        access_token=context.auth_provider.login(),
        options=None
    ))
    
    if isinstance(result, Js7LicenseInfo_V_2_8_2):
        return bool(result.valid), result.model_dump(mode="json")
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")
