from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.role.rename import rename, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    RoleRename as RoleRename_V_2_6_5
)


def rename_role_action(
    *,
    context: Context,
    identity_service_name: str,
    role_name: str,
    new_role_name: str,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            role_name=role_name,
            new_role_name=new_role_name,
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
    role_name: str,
    new_role_name: str,
    audit_log: Optional[AuditLog]
) -> RoleRename_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    # Validate: new_role_name
    if not new_role_name:
        raise ValueError("'new_role_name' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return RoleRename_V_2_6_5(
        identity_service_name=identity_service_name,
        role_old_name=role_name,
        role_new_name=new_role_name,
        audit_log=res_audit_log
    )