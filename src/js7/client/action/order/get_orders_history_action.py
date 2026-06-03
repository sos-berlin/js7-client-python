from typing import Any, Dict, List

from ...context import Context
from ....api.joc.http.v_2_6_5.orders.history import history, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.filter.order_history_filter import OrderHistoryFilter
from ....model.private.http.joc.joc_v_2_6_5 import (
    OrdersFilter as OrdersFilter_V_2_6_5,
    Folder as Folder_V_2_6_5,
    HistoryStateText as HistoryStateText_V_2_6_5
)


def get_orders_history_action(*, context: Context, controller_id: str, filter: OrderHistoryFilter) -> List[Dict[str, Any]]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            timezone=context.client_config.timezone,
            filter=filter
        )

        result = history(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.model_dump(mode="json").get("history") or []
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str,
    timezone: str,
    filter: OrderHistoryFilter
) -> OrdersFilter_V_2_6_5:
    
    # Validates controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: timezone
    if not timezone:
        raise ValueError("'timezone' is required in client configuration.")
        
    # Result
    return OrdersFilter_V_2_6_5(
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
            Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
            for f in filter.folders
        ] if filter.folders else None,
        
        history_states=[
            HistoryStateText_V_2_6_5(s)
            for s in filter.history_states
        ] if filter.history_states else None,
        
        compact=None,
        exclude_workflows=None,
        history_ids=None,
        orders=None,
        workflow_path=None
    )