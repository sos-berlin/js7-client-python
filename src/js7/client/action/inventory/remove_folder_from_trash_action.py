from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.inventory.trash.delete.folder import folder, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5, 
    CommonRequestFolder as CommonRequestFolder_V_2_6_5
)


def remove_folder_from_trash_action(
    *, 
    context: Context, 
    folder_path: str,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            folder_path=folder_path, 
            audit_log=audit_log
        )

        result = folder(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    folder_path: str,
    audit_log: Optional[AuditLog]
) -> CommonRequestFolder_V_2_6_5:

    # Validate: folder_path
    if not folder_path:
        raise ValueError("'folder_path' is required.") 
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return CommonRequestFolder_V_2_6_5(
        path=folder_path,
        audit_log=res_audit_log,
        recursive=True,
        
        controller_id=None,
        object_types=None,
        only_valid_objects=None,
    )