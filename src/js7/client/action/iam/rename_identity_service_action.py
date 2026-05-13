from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.identity_service.rename import rename, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    IdentityServiceRename as IdentityServiceRename_V_2_6_5
)


def rename_identity_service_action(
    *,
    context: Context,
    identity_service_name: str,
    new_identity_service_name: str,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            new_identity_service_name=new_identity_service_name,
            audit_log=audit_log
        )

        result = rename(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str,
    new_identity_service_name: str,
    audit_log: Optional[AuditLog]
) -> IdentityServiceRename_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: new_identity_service_name
    if not new_identity_service_name:
        raise ValueError("'new_identity_service_name' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return IdentityServiceRename_V_2_6_5(
        identity_service_old_name=identity_service_name,
        identity_service_new_name=new_identity_service_name,
        audit_log=res_audit_log
    )