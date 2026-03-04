from typing import List

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    RoleListFilter as RoleListFilter_V_2_8_2,
    Roles as Roles_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_roles_action(
    *, 
    context: Context,
    identity_service_name: str
) -> List[str]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/roles", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, Roles_V_2_8_2):
        return [
            r.role_name
            for r in result.roles
        ] if result.roles else []
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    identity_service_name: str
) -> RoleListFilter_V_2_8_2:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Result
    return RoleListFilter_V_2_8_2(
        identity_service_name=identity_service_name
    )