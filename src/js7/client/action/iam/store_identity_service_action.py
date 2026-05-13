from typing import Optional

from ...context import Context
from ....model.public.client.common.identity_service import IdentityService
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.identity_service.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    IdentityService as IdentityService_V_2_6_5,
    IdentityServiceType as IdentityServiceType_V_2_6_5,
    ServiceAuthenticationScheme as ServiceAuthenticationScheme_V_2_6_5
)


def store_identity_service_action(
    *,
    context: Context,
    identity_service: IdentityService,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service=identity_service,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service: IdentityService,
    audit_log: Optional[AuditLog]
) -> IdentityService_V_2_6_5:

    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return IdentityService_V_2_6_5(
        identity_service_name=identity_service.identity_service_name,
        # Raises ValueError() if invalid.
        identity_service_type=IdentityServiceType_V_2_6_5(identity_service.identity_service_type), 
        # Raises ValueError() if invalid.
        service_authentication_scheme=ServiceAuthenticationScheme_V_2_6_5(identity_service.service_authentication_scheme),
        second_factor=identity_service.second_factor,
        second_factor_identity_service_name=identity_service.second_factor_identity_service_name,
        disabled=identity_service.disabled,
        required=identity_service.required,
        ordering=identity_service.ordering,
        audit_log=res_audit_log
    )