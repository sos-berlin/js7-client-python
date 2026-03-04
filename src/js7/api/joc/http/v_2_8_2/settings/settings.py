from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import Configuration200


def settings(call: EndpointCall) -> Configuration200:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/settings", 
            body=None,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Configuration200.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="settings",
    function=settings,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Configuration200,
    options=None
)