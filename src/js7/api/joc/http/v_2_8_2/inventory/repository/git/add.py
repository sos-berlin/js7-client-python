from ........model.private.api.endpoint import EndpointDefinition, EndpointCall
from ........model.private.http.joc.joc_v_2_8_2 import CommonFilter, GitCommandResponse


def add(call: EndpointCall) -> GitCommandResponse:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, CommonFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.CommonFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/repository/git/add",
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return GitCommandResponse.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/repository/git/add",
    function=add,
    version=("2.6.5", "2.8.3"),
    payload_model=CommonFilter,
    response_model=GitCommandResponse,
    options=None
)