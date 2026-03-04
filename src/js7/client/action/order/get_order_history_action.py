from typing import Any, Dict

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.filter.order_history_filter import OrderHistoryFilter
from ....model.private.http.joc.joc_v_2_8_2 import (
    OrdersFilter as OrdersFilter_V_2_8_2,
    OrderHistory as OrderHistory_V_2_8_2,
    Folder as Folder_V_2_8_2,
    HistoryStateText as HistoryStateText_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_order_history_action(*, context: Context, controller_id: str, filter: OrderHistoryFilter) -> Dict[str, Any]:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            timezone=context.client_config.timezone,
            filter=filter
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="orders/history", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OrderHistory_V_2_8_2):
        return result.model_dump()
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    controller_id: str,
    timezone: str,
    filter: OrderHistoryFilter
) -> OrdersFilter_V_2_8_2:
    
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: timezone
    if not timezone:
        raise ValueError("'timezone' is required in client configuration.")
        
    # Result
    return OrdersFilter_V_2_8_2(
        controller_id=controller_id,
        date_from=filter.date_from,
        date_to=filter.date_to,
        completed_date_from=filter.completed_date_from,
        completed_date_to=filter.completed_date_to,
        time_zone=timezone,
        order_id=filter.order_id,
        workflow_name=filter.workflow_name,
        limit=filter.limit,
        
        folders=[
            Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
            for f in filter.folders
        ] if filter.folders else None,
        
        history_states=[
            HistoryStateText_V_2_8_2(s)
            for s in filter.history_states
        ] if filter.history_states else None,
        
        compact=None,
        exclude_workflows=None,
        history_ids=None,
        orders=None,
        workflow_path=None
    )