from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.role.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    RoleStore as RoleStore_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def store_role_action(
    *, 
    context: Context,
    identity_service_name: str,
    role_name: str,
    ordering: Optional[int],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            role_name=role_name,
            ordering=ordering,
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
    identity_service_name: str,
    role_name: str,
    ordering: Optional[int],
    audit_log: Optional[AuditLog]
) -> RoleStore_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return RoleStore_V_2_6_5(
        identity_service_name=identity_service_name,
        role_name=role_name,
        ordering=ordering,
        audit_log=res_audit_log
    )