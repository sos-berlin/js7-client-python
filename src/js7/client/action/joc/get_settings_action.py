from typing import Any, Dict
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import Configuration200 as Configuration200_V_2_8_2


def get_settings_action(*, context: Context) -> Dict[str, Any]:        
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="settings", call=EndpointCall(
        http_service=context.http_service,
        payload=None,
        access_token=context.auth_provider.login(),
        options=None
    ))
    
    if isinstance(result, Configuration200_V_2_8_2):
        return result.model_dump(mode="json")

    raise ValueError("JOC returned no version information.")