from ......model.private.api.endpoint import EndpointCall, EndpointDefinition
from ......model.private.http.joc.joc_v_2_8_2 import AddOrders, OrderIDS


def add(call: EndpointCall) -> OrderIDS:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not isinstance(call.payload, AddOrders):
        raise TypeError("'payload' is not an instance of model.http.joc_v_2_8_2.AddOrders")
        
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)

    with call.http_service as http:
        resp = http.post(
            path="/joc/api/orders/add",
            body=body,
            headers={
                "X-Access-Token": call.access_token,
                "Accept": "application/json"
            }
        )
        
        return OrderIDS.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="orders/add",
    function=add,
    version=("2.6.5", "2.8.3"),
    payload_model=AddOrders,
    response_model=OrderIDS,
    options=None
)