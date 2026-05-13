from typing import Optional

from ...context import Context
from ....model.public.client.filter.element.folder import Folder
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.folder.rename import rename, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    FolderRename as FolderRename_V_2_6_5,
    Folder as Folder_V_2_6_5
)


def rename_folder_permissions_action(
    *,
    context: Context,
    identity_service_name: str,
    folder_name: str,
    new_folder: Folder,
    controller_id: str,
    role_name: str,
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            folder_name=folder_name,
            new_folder=new_folder,
            controller_id=controller_id,
            role_name=role_name,
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
    folder_name: str,
    new_folder: Folder,
    controller_id: str,
    role_name: str,
    audit_log: Optional[AuditLog]
) -> FolderRename_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: folder_name
    if not folder_name:
        raise ValueError("'folder_name' is required.")
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
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
    return FolderRename_V_2_6_5(
        identity_service_name=identity_service_name,
        old_folder_name=folder_name,
        new_folder=Folder_V_2_6_5(
            folder=new_folder.folder_path, 
            recursive=new_folder.recursive
        ),
        controller_id=controller_id,
        role_name=role_name,
        audit_log=res_audit_log
    )