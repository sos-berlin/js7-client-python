import json
from typing import Any, Dict, Literal

from ...context import Context
from ....api.joc.http.v_2_6_5.configuration.save import save, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    Configuration as Configuration_V_2_6_5,
    ConfigurationType as ConfigurationType_V_2_6_5
)


def store_identity_service_settings_action(
    *,
    context: Context,
    identity_service_name: str,
    identity_service_type: Literal["KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"],
    settings: Dict[str, Any]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            identity_service_type=identity_service_type,
            settings=settings
        )

        result = save(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.id)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str,
    identity_service_type: Literal["KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"],
    settings: Dict[str, Any]
) -> Configuration_V_2_6_5:
    
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
    return Configuration_V_2_6_5(
        id=0,
        name=identity_service_name,
        object_type=identity_service_type,
        configuration_type=ConfigurationType_V_2_6_5.IAM,
        configuration_item=json.dumps(settings),
    )