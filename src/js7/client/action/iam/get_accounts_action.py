from typing import List, Optional

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.accounts import Account
from ....model.private.http.joc.joc_v_2_8_2 import (
    AccountListFilter as AccountListFilter_V_2_8_2,
    Accounts as Accounts_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_accounts_action(
    *, 
    context: Context,
    identity_service_name: str,
    filter_account_name: Optional[str],
    filter_enabled: bool,
    filter_disabled: bool
) -> List[Account]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            identity_service_name=identity_service_name,
            filter_account_name=filter_account_name,
            filter_enabled=filter_enabled,
            filter_disabled=filter_disabled
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/accounts", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, Accounts_V_2_8_2):
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
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    identity_service_name: str,
    filter_account_name: Optional[str],
    filter_enabled: bool,
    filter_disabled: bool
) -> AccountListFilter_V_2_8_2:

    # Validate: identity_service_name
    if not identity_service_name:
        raise ValueError("'identity_service_name' is required.")

    # Result
    return AccountListFilter_V_2_8_2(
        account_name=filter_account_name,
        disabled=filter_disabled,
        enabled=filter_enabled,
        identity_service_name=identity_service_name
    )