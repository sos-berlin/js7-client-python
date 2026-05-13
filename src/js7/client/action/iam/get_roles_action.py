from typing import List

from ...context import Context
from ....api.joc.http.v_2_6_5.iam.roles.roles import roles, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    RoleListFilter as RoleListFilter_V_2_6_5
)


def get_roles_action(
    *, 
    context: Context,
    identity_service_name: str
) -> List[str]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name
        )

        result = roles(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        result_list: List[str] = []
        if result.roles:
            for r in result.roles:
                if not r.role_name:
                    continue
                result_list.append(r.role_name)
        return result_list
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str
) -> RoleListFilter_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Result
    return RoleListFilter_V_2_6_5(
        identity_service_name=identity_service_name
    )