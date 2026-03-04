from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import Version as Version_V_2_8_2


def get_version_action(*, context: Context) -> str:        
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="joc/version", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
    ))
    
    if isinstance(result, Version_V_2_8_2):
        if result.version:
            return result.version

    raise ValueError("JOC returned no version information.")