from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.account.change_password import change_password, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    AccountChangePassword as AccountChangePassword_V_2_6_5
)


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

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            account_name=account_name,
            account_password=account_password,
            new_account_password=new_account_password,
            force_password_change=force_password_change,
            audit_log=audit_log
        )

        result = change_password(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str,
    account_name: str,
    account_password: str,
    new_account_password: str,
    force_password_change: bool,
    audit_log: Optional[AuditLog]
) -> AccountChangePassword_V_2_6_5:

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
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return AccountChangePassword_V_2_6_5(
        identity_service_name=identity_service_name,
        account_name=account_name,
        old_password=account_password,
        password=new_account_password,
        repeated_password=new_account_password,
        force_password_change=force_password_change,
        audit_log=res_audit_log
    )