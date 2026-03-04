from ......model.private.api.endpoint import EndpointCall, EndpointDefinition
from ......model.private.http.joc.joc_v_2_8_2 import GetDependenciesRequest, GetDependenciesResponse


def dependencies(call: EndpointCall) -> GetDependenciesResponse:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not isinstance(call.payload, GetDependenciesRequest):
        raise TypeError("'payload' is not an instance of model.http.joc_v_2_8_2.GetDependenciesRequest")
        
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/dependencies",
            body=body,
            headers={
                "X-Access-Token": call.access_token,
                "Accept": "application/json"
            }
        )
        
        return GetDependenciesResponse.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/dependencies",
    function=dependencies,
    version=("2.6.5", "2.8.3"),
    payload_model=GetDependenciesRequest,
    response_model=GetDependenciesResponse,
    options=None
)