from typing import List, Optional, Union

from ...context import Context
from ....model.public.client.filter.element.folder import Folder
from ....api.joc.http.v_2_6_5.iam.folders.folders import folders, EndpointCall as FoldersEndpointCall
from ....api.joc.http.v_2_6_5.iam.folder.folder import folder, EndpointCall as FolderEndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    FolderListFilter as FolderListFilter_V_2_6_5,
    Folders as Folders_V_2_6_5,
    FolderFilter as FolderFilter_V_2_6_5,
    FolderItem as FolderItem_V_2_6_5
)


def get_folder_permissions_action(
    *, 
    context: Context,
    identity_service_name: str,
    folder_name: Optional[str],
    role_name: str,
    controller_id: str
) -> List[Folder]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = _build_v_2_6_5_request(
            context=context,
            identity_service_name=identity_service_name,
            folder_name=folder_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        if isinstance(result, Folders_V_2_6_5):    
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
        
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    context: Context,
    identity_service_name: str,
    folder_name: Optional[str],
    role_name: str,
    controller_id: str
) -> Union[Folders_V_2_6_5, FolderItem_V_2_6_5]:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: role_name
    if not role_name:
        raise ValueError("'role_name' is required.")
    
    if not folder_name:
        # Build: folders_req
        folders_req = FolderListFilter_V_2_6_5(
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id
        )
        
        folders_res = folders(FoldersEndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=folders_req,
        ))
        
        return folders_res
    
    # Build: folder_req
    folder_req = FolderFilter_V_2_6_5(
        identity_service_name=identity_service_name,
        role_name=role_name,
        controller_id=controller_id,
        folder_name=folder_name
    )
    
    folder_res = folder(FolderEndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=folder_req
    ))
    
    return folder_res