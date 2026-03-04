from ......model.private.api.endpoint import EndpointCall, EndpointDefinition
from ......model.private.http.joc.joc_v_2_8_2 import Version


def version(call: EndpointCall) -> Version:    
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/joc/version", 
            body=None,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Version.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="joc/version",
    function=version,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Version,
    options=None
)