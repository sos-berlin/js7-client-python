from datetime import datetime
from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.accounts import BlockedAccount
from ....model.private.http.joc.joc_v_2_8_2 import (
    BlockedAccountsFilter as BlockedAccountsFilter_V_2_8_2,
    BlockedAccounts as BlockedAccounts_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def get_blocked_accounts_action(
    *, 
    context: Context,
    filter_date_from: Optional[datetime],
    filter_date_to: Optional[datetime],
    filter_account_name: Optional[str]
) -> List[BlockedAccount]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            timezone=context.client_config.timezone,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            filter_account_name=filter_account_name
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="iam/blockedAccounts", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, BlockedAccounts_V_2_8_2):
        return [
            BlockedAccount(
                account_name=a.account_name,
                comment=a.comment,
                blocked_since=a.since,
                audit_log=AuditLog(
                    comment=a.audit_log.comment,
                    ticket_link=a.audit_log.ticket_link,
                    time_spent=a.audit_log.time_spent
                ) if a.audit_log else None
            )
            for a in result.blocked_accounts
        ] if result.blocked_accounts else []
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    timezone: str,
    filter_date_from: Optional[datetime],
    filter_date_to: Optional[datetime],
    filter_account_name: Optional[str]
) -> BlockedAccountsFilter_V_2_8_2:

    # Result
    return BlockedAccountsFilter_V_2_8_2(
        time_zone=timezone,
        date_from=filter_date_from,
        date_to=filter_date_to,
        account_name=filter_account_name
    )