from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import VersionsFilter, VersionResponse


def versions(call: EndpointCall) -> VersionResponse:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, VersionsFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.VersionsFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/joc/versions", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return VersionResponse.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="joc/versions",
    function=versions,
    version=("2.6.5", "2.8.3"),
    payload_model=VersionsFilter,
    response_model=VersionResponse,
    options=None
)