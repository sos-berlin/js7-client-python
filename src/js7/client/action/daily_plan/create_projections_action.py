from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    OK as OK_V_2_8_2
)


def create_projections_action(
    *,
    context: Context
) -> bool:
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/projections/recreate", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=None,
        options=None
    ))

    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")
