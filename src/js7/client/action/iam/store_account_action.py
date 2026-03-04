from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.accounts import Account
from ....model.private.http.joc.joc_v_2_8_2 import (
    Account as Account_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_account_action(
    *,
    context: Context,
    account: Account,
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            account=account,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/account/store", call=EndpointCall(
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
    account: Account,
    audit_log: Optional[AuditLog]
) -> Account_V_2_8_2:

    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return Account_V_2_8_2(
        account_name=account.account_name,
        password=account.password,
        disabled=account.disabled,
        force_password_change=account.force_password_change,
        identity_service_name=account.identity_service_name,
        roles=account.roles,
        audit_log=res_audit_log
    )