from typing import Optional

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    RequestFolder as RequestFolder_V_2_8_2,
    OK as OK_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def remove_folder_action(
    *, 
    context: Context, 
    folder_path: str,
    audit_log: Optional[AuditLog]
) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(folder_path=folder_path, audit_log=audit_log) 
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/remove/folder", call=EndpointCall(
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
    folder_path: str,
    audit_log: Optional[AuditLog]
) -> RequestFolder_V_2_8_2:
    
    # Validate: folder_path
    if not folder_path:
        raise ValueError("'folder_path' is required.") 
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    return RequestFolder_V_2_8_2(
        path=folder_path,
        audit_log=res_audit_log,
        
        cancel_orders_date_from=None, # Not the right domain here.
        controller_id=None,
        recursive=True,
        object_types=None,
        only_valid_objects=False,
    )