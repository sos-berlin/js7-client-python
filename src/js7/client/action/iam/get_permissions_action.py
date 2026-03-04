from typing import List, Optional, Tuple, Union

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    PermissionListFilter as PermissionListFilter_V_2_8_2,
    Permissions as Permissions_V_2_8_2,
    PermissionItem as PermissionItem_V_2_8_2,
    PermissionFilter as PermissionFilter_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_permissions_action(
    *, 
    context: Context,
    permission_path: Optional[str],
    identity_service_name: str,
    role_name: str,
    controller_id: Optional[str],
    without_excluded: bool
) -> List[Tuple[str, bool]]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        result = _build_v_2_8_2_request(
            context=context,
            permission_path=permission_path,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        permissions: List[Tuple[str, bool]] = []
        
        if isinstance(result, Permissions_V_2_8_2):    
            for p in result.permissions:
                if p.excluded is True and without_excluded:
                    continue
                
                permissions.append((p.permission_path, p.excluded or False))
        else:
            if result.permission:
                if result.permission.excluded is True and without_excluded:
                    return permissions
                
                permissions.append((result.permission.permission_path, result.permission.excluded or False))
            
        return permissions
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    context: Context,
    permission_path: Optional[str],
    identity_service_name: str,
    role_name: str,
    controller_id: Optional[str]
) -> Union[PermissionItem_V_2_8_2, Permissions_V_2_8_2]:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    if not permission_path:
        # Build: permissions_req
        permissions_req = PermissionListFilter_V_2_8_2(
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        # Calls the dispatcher for the matching JOC version
        permissions_res = context.joc_api.dispatch(endpoint_id="iam/permissions", call=EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=permissions_req,
            options=None,
        ))
        
        if not isinstance(permissions_res, Permissions_V_2_8_2):
            raise RuntimeError(f"Unexpected response type: {type(permissions_res).__name__}")
        
        return permissions_res
    
    # Build: permission_req
    permission_req = PermissionFilter_V_2_8_2(
        identity_service_name=identity_service_name,
        role_name=role_name,
        controller_id=controller_id,
        permission_path=permission_path
    )
    
    # Calls the dispatcher for the matching JOC version
    permission_res = context.joc_api.dispatch(endpoint_id="iam/permission", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=permission_req,
        options=None,
    ))
    
    if not isinstance(permission_res, PermissionItem_V_2_8_2):
        raise RuntimeError(f"Unexpected response type: {type(permission_res).__name__}")
    
    return permission_res