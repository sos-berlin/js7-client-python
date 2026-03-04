from .........model.private.api.endpoint import EndpointDefinition, EndpointCall
from .........model.private.http.joc.joc_v_2_8_2 import GitCredentials


def credentials(call: EndpointCall) -> GitCredentials:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/repository/git/credentials",
            body=None,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return GitCredentials.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/repository/git/credentials",
    function=credentials,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=GitCredentials,
    options=None
)