from typing import List, Optional, Tuple

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    Permissions as Permissions_V_2_8_2,
    Permission as Permission_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def set_permissions_action(
    *,
    context: Context,
    identity_service_name: str,
    role_name: str,
    controller_id: str,
    permissions: List[Tuple[str, bool]],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id,
            permissions=permissions,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/permissions/store", call=EndpointCall(
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
    identity_service_name: str,
    role_name: str,
    controller_id: str,
    permissions: List[Tuple[str, bool]],
    audit_log: Optional[AuditLog]
) -> Permissions_V_2_8_2:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return Permissions_V_2_8_2(
        identity_service_name=identity_service_name,
        role_name=role_name,
        controller_id=controller_id,
        permissions=[
            Permission_V_2_8_2(permission_path=p, excluded=e)
            for p, e in permissions
        ],
        audit_log=res_audit_log
    )