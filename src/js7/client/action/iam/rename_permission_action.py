from typing import Optional, Tuple

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    PermissionRename as PermissionRename_V_2_8_2,
    Permission as Permission_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def rename_permission_action(
    *,
    context: Context,
    identity_service_name: str,
    permission_path: str,
    new_permission: Tuple[str, bool],
    role_name: str,
    controller_id: str,
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name,
            permission_path=permission_path,
            new_permission=new_permission,
            role_name=role_name,
            controller_id=controller_id,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/permission/rename", call=EndpointCall(
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
    permission_path: str,
    new_permission: Tuple[str, bool],
    role_name: str,
    controller_id: str,
    audit_log: Optional[AuditLog]
) -> PermissionRename_V_2_8_2:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: permission_path
    if not permission_path:
        raise ValueError("'permission_path' is required.")
    
    # Validate: new_permission
    if not new_permission:
        raise ValueError("'new_permission' is required.")
    
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
    return PermissionRename_V_2_8_2(
        identity_service_name=identity_service_name,
        old_permission_path=permission_path,
        new_permission=Permission_V_2_8_2(
            permission_path=new_permission[0],
            excluded=new_permission[1]
        ),
        role_name=role_name,
        controller_id=controller_id,
        audit_log=res_audit_log
    )