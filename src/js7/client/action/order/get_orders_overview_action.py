from typing import Optional, Tuple

from ...context import Context
from ....api.joc.http.v_2_6_5.orders.overview.summary import summary, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    OrdersFilter as OrdersFilter_V_2_6_5
)


def get_orders_overview_action(
    *,
    context: Context, 
    controller_id: Optional[str],
    date_from: Optional[str],
    date_to: Optional[str]
) -> Tuple[int, int]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            date_from=date_from,
            date_to=date_to,
            timezone=context.client_config.timezone
        )

        result = summary(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        successful = result.orders.successful or 0 if result.orders else 0
        failed = result.orders.failed or 0 if result.orders else 0
        
        return (successful, failed)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: Optional[str],
    date_from: Optional[str],
    date_to: Optional[str],
    timezone: Optional[str]
) -> OrdersFilter_V_2_6_5:

    # Result
    return OrdersFilter_V_2_6_5(
        controller_id=controller_id,
        date_from=date_from,
        date_to=date_to,
        time_zone=timezone
    )
