from datetime import datetime
from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.iam.blocked_accounts.blocked_accounts import blocked_accounts, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.accounts import BlockedAccount
from ....model.private.http.joc.joc_v_2_6_5 import (
    BlockedAccountsFilter as BlockedAccountsFilter_V_2_6_5
)


def get_blocked_accounts_action(
    *, 
    context: Context,
    filter_date_from: Optional[datetime],
    filter_date_to: Optional[datetime],
    filter_account_name: Optional[str]
) -> List[BlockedAccount]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            timezone=context.client_config.timezone,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            filter_account_name=filter_account_name
        )

        result = blocked_accounts(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
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
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    timezone: str,
    filter_date_from: Optional[datetime],
    filter_date_to: Optional[datetime],
    filter_account_name: Optional[str]
) -> BlockedAccountsFilter_V_2_6_5:

    # Result
    return BlockedAccountsFilter_V_2_6_5(
        time_zone=timezone,
        date_from=filter_date_from,
        date_to=filter_date_to,
        account_name=filter_account_name
    )