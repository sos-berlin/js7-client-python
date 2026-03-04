from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    BlockedAccount as BlockedAccount_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def block_account_action(
    *,
    context: Context,
    account_name: str,
    comment: Optional[str],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            account_name=account_name,
            comment=comment,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/blockedAccount/store", call=EndpointCall(
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
    account_name: str,
    comment: Optional[str],
    audit_log: Optional[AuditLog]
) -> BlockedAccount_V_2_8_2:
    
    # Validate: account_name
    if not account_name:
        raise ValueError("'account_name' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return BlockedAccount_V_2_8_2(
        account_name=account_name,
        audit_log=res_audit_log,
        comment=comment,
    )