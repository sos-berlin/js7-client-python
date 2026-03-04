from ......model.private.http.joc.joc_v_2_8_2 import Permissions
from ......model.private.api.endpoint import EndpointCall, EndpointDefinition


def joc_cockpit_permissions(call: EndpointCall) -> Permissions:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/authentication/joc_cockpit_permissions", 
            body=None, 
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Permissions.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="authentication/joc_cockpit_permissions",
    function=joc_cockpit_permissions,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Permissions,
    options=None
)