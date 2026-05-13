from typing import List, Optional

from ...context import Context
from ....api.joc.http.v_2_6_5.iam.accounts.accounts import accounts, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.accounts import Account
from ....model.private.http.joc.joc_v_2_6_5 import (
    AccountListFilter as AccountListFilter_V_2_6_5
)


def get_accounts_action(
    *, 
    context: Context,
    identity_service_name: str,
    filter_account_name: Optional[str],
    filter_enabled: bool,
    filter_disabled: bool
) -> List[Account]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            identity_service_name=identity_service_name,
            filter_account_name=filter_account_name,
            filter_enabled=filter_enabled,
            filter_disabled=filter_disabled
        )

        result = accounts(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return [
            Account(
                account_name=a.account_name,
                disabled=a.disabled,
                force_password_change=a.force_password_change,
                identity_service_name=a.identity_service_name,
                roles=a.roles
            )
            for a in result.account_items
        ] if result.account_items else []
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    identity_service_name: str,
    filter_account_name: Optional[str],
    filter_enabled: bool,
    filter_disabled: bool
) -> AccountListFilter_V_2_6_5:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")

    # Result
    return AccountListFilter_V_2_6_5(
        account_name=filter_account_name,
        disabled=filter_disabled,
        enabled=filter_enabled,
        identity_service_name=identity_service_name
    )