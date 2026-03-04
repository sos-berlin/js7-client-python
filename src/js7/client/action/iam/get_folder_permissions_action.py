from typing import List, Optional, Union

from ...context import Context
from ....model.public.client.filter.element.folder import Folder
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    FolderListFilter as FolderListFilter_V_2_8_2,
    Folders as Folders_V_2_8_2,
    FolderFilter as FolderFilter_V_2_8_2,
    FolderItem as FolderItem_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_folder_permissions_action(
    *, 
    context: Context,
    identity_service_name: str,
    folder_name: Optional[str],
    role_name: str,
    controller_id: str
) -> List[Folder]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        result = _build_v_2_8_2_request(
            context=context,
            identity_service_name=identity_service_name,
            folder_name=folder_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        if isinstance(result, Folders_V_2_8_2):    
            return [
                Folder(
                    folder_path=f.folder,
                    recursive=f.recursive or False
                )
                for f in result.folders
            ]
        else:
            return [
                Folder(
                    folder_path=result.folder.folder,
                    recursive=result.folder.recursive or False
                )
            ] if result.folder else []
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    context: Context,
    identity_service_name: str,
    folder_name: Optional[str],
    role_name: str,
    controller_id: str
) -> Union[Folders_V_2_8_2, FolderItem_V_2_8_2]:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    if not folder_name:
        # Build: folders_req
        folders_req = FolderListFilter_V_2_8_2(
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        # Calls the dispatcher for the matching JOC version
        folders_res = context.joc_api.dispatch(endpoint_id="iam/folders", call=EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=folders_req,
            options=None,
        ))
        
        if not isinstance(folders_res, Folders_V_2_8_2):
            raise RuntimeError(f"Unexpected response type: {type(folders_res).__name__}")
        
        return folders_res
    
    # Build: folder_req
    folder_req = FolderFilter_V_2_8_2(
        identity_service_name=identity_service_name,
        role_name=role_name,
        controller_id=controller_id,
        folder_name=folder_name
    )
    
    # Calls the dispatcher for the matching JOC version
    folder_res = context.joc_api.dispatch(endpoint_id="iam/folder", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=folder_req,
        options=None,
    ))
    
    if not isinstance(folder_res, FolderItem_V_2_8_2):
        raise RuntimeError(f"Unexpected response type: {type(folder_res).__name__}")
    
    return folder_res