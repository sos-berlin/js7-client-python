from typing import Any, Dict, Optional

from ....model.public.client.common.configurations import Configuration
from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    ConfigurationObject as ConfigurationObject_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
)


def store_configuration_action(
    *, 
    context: Context,
    configuration: Configuration,
    payload: Optional[Dict[str, Any]],
    no_invalid: bool,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            configuration=configuration, 
            payload=payload,
            no_invalid=no_invalid,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        if result.valid is False:
            raise ValueError(f"Configuration is invalid: {result.invalid_msg}")
        return True
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    configuration: Configuration, 
    payload: Optional[Dict[str, Any]],
    no_invalid: bool,
    audit_log: Optional[AuditLog]
) -> ConfigurationObject_V_2_6_5:

    # Validate: payload
    if configuration.object_type.value != "FOLDER" and not payload:
        raise ValueError("'payload' is required.")

    # Build: Audit log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
            
    # Result
    return ConfigurationObject_V_2_6_5(
        path=configuration.path,
        object_type=ConfigurationType_V_2_6_5(configuration.object_type.value), # Raises ValueError() if invalid.
        configuration=payload,
        audit_log=res_audit_log,
        valid=no_invalid,
    )
