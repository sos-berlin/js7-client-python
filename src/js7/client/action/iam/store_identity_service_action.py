from typing import Optional

from ...context import Context
from ....model.public.client.common.identity_service import IdentityService
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    IdentityService as IdentityService_V_2_8_2,
    IdentityServiceType as IdentityServiceType_V_2_8_2,
    ServiceAuthenticationScheme as ServiceAuthenticationScheme_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_identity_service_action(
    *,
    context: Context,
    identity_service: IdentityService,
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service=identity_service,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/identityservice/store", call=EndpointCall(
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
    identity_service: IdentityService,
    audit_log: Optional[AuditLog]
) -> IdentityService_V_2_8_2:

    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return IdentityService_V_2_8_2(
        identity_service_name=identity_service.identity_service_name,
        # Raises ValueError() if invalid.
        identity_service_type=IdentityServiceType_V_2_8_2(identity_service.identity_service_type), 
        # Raises ValueError() if invalid.
        service_authentication_scheme=ServiceAuthenticationScheme_V_2_8_2(identity_service.service_authentication_scheme),
        second_factor=identity_service.second_factor,
        second_factor_identity_service_name=identity_service.second_factor_identity_service_name,
        disabled=identity_service.disabled,
        required=identity_service.required,
        ordering=identity_service.ordering,
        audit_log=res_audit_log
    )