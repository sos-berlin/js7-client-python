from typing import List, Optional

from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.configurations import Configuration
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    RequestFilters as RequestFilters_V_2_8_2,
    OK as OK_V_2_8_2,
    CommonRequestFilter as CommonRequestFilter_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def remove_configurations_action(
    *, 
    context: Context, 
    configurations: List[Configuration],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(configurations=configurations, audit_log=audit_log) 
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/remove", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    configurations: List[Configuration],
    audit_log: Optional[AuditLog]
) -> RequestFilters_V_2_8_2:

    # Validate: configurations
    if not configurations:
        raise ValueError("'configurations' are required.")
    
    # Build: res_object
    res_object = [
        CommonRequestFilter_V_2_8_2(
            path=c.path,
            object_type=ConfigurationType_V_2_8_2(c.object_type.value) # Raises ValueError() if invalid.
        )
        for c in configurations
    ]
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    return RequestFilters_V_2_8_2(
        objects=res_object,
        audit_log=res_audit_log,
        
        cancel_orders_date_from=None, # Not the correct domain
    )