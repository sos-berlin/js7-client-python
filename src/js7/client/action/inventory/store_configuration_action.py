from typing import Any, Dict, Optional

from ....model.public.client.common.configurations import Configuration
from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    ConfigurationObject as ConfigurationObject_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def store_configuration_action(
    *, 
    context: Context,
    configuration: Configuration,
    payload: Optional[Dict[str, Any]],
    no_invalid: bool,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            configuration=configuration, 
            payload=payload,
            no_invalid=no_invalid,
            audit_log=audit_log,
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/store", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, ConfigurationObject_V_2_8_2):
        if result.valid is False:
            raise ValueError(f"Configuration is invalid: {result.invalid_msg}")
        return True

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    configuration: Configuration, 
    payload: Optional[Dict[str, Any]],
    no_invalid: bool,
    audit_log: Optional[AuditLog]
) -> ConfigurationObject_V_2_8_2:

    # Validate: payload
    if configuration.object_type.value != "FOLDER" and not payload:
        raise ValueError("'payload' is required.")

    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
            
    # Result
    return ConfigurationObject_V_2_8_2(
        path=configuration.path,
        object_type=ConfigurationType_V_2_8_2(configuration.object_type.value), # Raises ValueError() if invalid.
        configuration=payload,
        audit_log=res_audit_log,
        valid=no_invalid,
    )
