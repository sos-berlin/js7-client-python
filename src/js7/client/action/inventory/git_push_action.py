from typing import Literal, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    CommonFilter as CommonFilter_V_2_8_2,
    Category as Category_V_2_8_2,
    GitCommandResponse as GitCommandResponse_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def git_push_action(
    *,
    context: Context,
    folder_path: str,
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog],
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            folder_path=folder_path,
            category=category,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/git/push", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, GitCommandResponse_V_2_8_2):
        return bool(result.exit_code == 0)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    folder_path: str,
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog],
) -> CommonFilter_V_2_8_2:

    # Validates folder path
    if not folder_path:
        raise ValueError("'folder_path' is required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return CommonFilter_V_2_8_2(
        folder=folder_path,
        category=Category_V_2_8_2(category), # Raises ValueError() if invalid.
        audit_log=res_audit_log
    )