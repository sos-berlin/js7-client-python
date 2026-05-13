from typing import List, Optional, Tuple, Union

from ...context import Context
from ....api.joc.http.v_2_6_5.iam.permissions.permissions import permissions, EndpointCall as PermissionsEndpointCall
from ....api.joc.http.v_2_6_5.iam.permission.permission import permission, EndpointCall as PermissionEndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    PermissionListFilter as PermissionListFilter_V_2_6_5,
    Permissions as Permissions_V_2_6_5,
    PermissionItem as PermissionItem_V_2_6_5,
    PermissionFilter as PermissionFilter_V_2_6_5
)


def get_permissions_action(
    *, 
    context: Context,
    permission_path: Optional[str],
    identity_service_name: str,
    role_name: str,
    controller_id: Optional[str],
    without_excluded: bool
) -> List[Tuple[str, bool]]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = _build_v_2_6_5_request(
            context=context,
            permission_path=permission_path,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        permissions: List[Tuple[str, bool]] = []
        
        if isinstance(result, Permissions_V_2_6_5):    
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
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    context: Context,
    permission_path: Optional[str],
    identity_service_name: str,
    role_name: str,
    controller_id: Optional[str]
) -> Union[PermissionItem_V_2_6_5, Permissions_V_2_6_5]:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    if not permission_path:
        # Build: permissions_req
        permissions_req = PermissionListFilter_V_2_6_5(
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        permissions_res = permissions(PermissionsEndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=permissions_req
        ))
        
        return permissions_res
    
    # Build: permission_req
    permission_req = PermissionFilter_V_2_6_5(
        identity_service_name=identity_service_name,
        role_name=role_name,
        controller_id=controller_id,
        permission_path=permission_path
    )
    
    permission_res = permission(PermissionEndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=permission_req
    ))
    
    return permission_res