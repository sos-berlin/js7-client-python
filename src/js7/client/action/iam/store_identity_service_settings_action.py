import json
from typing import Any, Dict, Literal

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    Configuration as Configuration_V_2_8_2,
    ConfigurationType as ConfigurationType_V_2_8_2,
    ConfigurationOk as ConfigurationOk_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_identity_service_settings_action(
    *,
    context: Context,
    identity_service_name: str,
    identity_service_type: Literal["KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"],
    settings: Dict[str, Any]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name,
            identity_service_type=identity_service_type,
            settings=settings
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="configuration/save", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, ConfigurationOk_V_2_8_2):
        return bool(result.id)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    identity_service_name: str,
    identity_service_type: Literal["KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"],
    settings: Dict[str, Any]
) -> Configuration_V_2_8_2:
    
    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: identity_service_type
    if identity_service_type not in ["KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"]:
        raise ValueError(f"identity service type: {identity_service_type} is not supported.")
    
    # Validate: settings
    if not settings:
        raise ValueError("'settings' is required.")
    
    # Result
    return Configuration_V_2_8_2(
        id=0,
        name=identity_service_name,
        object_type=identity_service_type,
        configuration_type=ConfigurationType_V_2_8_2.IAM,
        configuration_item=json.dumps(settings),
    )