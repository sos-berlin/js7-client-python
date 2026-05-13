from typing import Any, Dict, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.account.permissions import permissions, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AccountFilter as AccountFilter_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def get_account_permissions_action(
    *, 
    context: Context,
    identity_service_name: str,
    account_name: str,
    audit_log: Optional[AuditLog]
) -> Dict[str, Any]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            account_name=account_name,
            audit_log=audit_log
        )

        result = permissions(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str,
    account_name: str,
    audit_log: Optional[AuditLog]
) -> AccountFilter_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")
    
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
    return AccountFilter_V_2_6_5(
        identity_service_name=identity_service_name,
        account_name=account_name,
        audit_log=res_audit_log
    )