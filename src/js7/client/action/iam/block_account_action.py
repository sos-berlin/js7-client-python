from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.blocked_account.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    BlockedAccount as BlockedAccount_V_2_6_5
)


def block_account_action(
    *,
    context: Context,
    account_name: str,
    comment: Optional[str],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            account_name=account_name,
            comment=comment,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    account_name: str,
    comment: Optional[str],
    audit_log: Optional[AuditLog]
) -> BlockedAccount_V_2_6_5:
    
    # Validate: account_name
    if not account_name:
        raise ValueError("'account_name' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return BlockedAccount_V_2_6_5(
        account_name=account_name,
        audit_log=res_audit_log,
        comment=comment,
    )