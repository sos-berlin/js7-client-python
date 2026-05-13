from typing import Literal, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.inventory.repository.git.push import push, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    CommonFilter as CommonFilter_V_2_6_5,
    Category as Category_V_2_6_5
)


def git_push_action(
    *,
    context: Context,
    folder_path: str,
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog],
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            folder_path=folder_path,
            category=category,
            audit_log=audit_log
        )

        result = push(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.exit_code == 0)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    folder_path: str,
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog],
) -> CommonFilter_V_2_6_5:

    # Validates folder path
    if not folder_path:
        raise ValueError("'folder_path' is required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return CommonFilter_V_2_6_5(
        folder=folder_path,
        category=Category_V_2_6_5(category), # Raises ValueError() if invalid.
        audit_log=res_audit_log
    )