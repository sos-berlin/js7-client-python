from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import OrdersFilter, OrderHistory


def history(call: EndpointCall) -> OrderHistory:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, OrdersFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.OrdersFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/orders/history", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return OrderHistory.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="orders/history",
    function=history,
    version=("2.6.5", "2.8.3"),
    payload_model=OrdersFilter,
    response_model=OrderHistory,
    options=None
)
