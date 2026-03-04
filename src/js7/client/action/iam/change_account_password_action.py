from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    AccountChangePassword as AccountChangePassword_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def change_account_password_action(
    *,
    context: Context,
    identity_service_name: str,
    account_name: str,
    account_password: str,
    new_account_password: str,
    force_password_change: bool,
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name,
            account_name=account_name,
            account_password=account_password,
            new_account_password=new_account_password,
            force_password_change=force_password_change,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/account/changepassword", call=EndpointCall(
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
    identity_service_name: str,
    account_name: str,
    account_password: str,
    new_account_password: str,
    force_password_change: bool,
    audit_log: Optional[AuditLog]
) -> AccountChangePassword_V_2_8_2:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
    # Validate: account_name
    if not account_name:
        raise ValueError("'account_name' is required.")
    
    # Validate: account_password
    if not account_password:
        raise ValueError("'account_password' is required.")
    
    # Validate: new_account_password
    if not new_account_password:
        raise ValueError("'new_account_password' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return AccountChangePassword_V_2_8_2(
        identity_service_name=identity_service_name,
        account_name=account_name,
        old_password=account_password,
        password=new_account_password,
        repeated_password=new_account_password,
        force_password_change=force_password_change,
        audit_log=res_audit_log
    )