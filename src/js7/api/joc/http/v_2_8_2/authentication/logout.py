from ......model.private.http.joc.joc_v_2_8_2 import Authentication
from ......model.private.api.endpoint import EndpointCall, EndpointDefinition


def logout(call: EndpointCall) -> Authentication:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/authentication/logout", 
            body=None, 
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Authentication.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="authentication/logout",
    function=logout,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Authentication,
    options=None
)