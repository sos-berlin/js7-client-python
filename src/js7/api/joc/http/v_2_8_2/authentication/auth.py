import json
from ......model.private.http.joc.joc_v_2_8_2 import SecurityConfiguration
from ......model.private.api.endpoint import EndpointCall, EndpointDefinition


def auth(call: EndpointCall) -> SecurityConfiguration:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options or not call.options.get("identity_service_name"):
        raise ValueError("'identity_service_name' is required in function options call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/authentication/auth", 
            body=json.dumps({ "identityServiceName": call.options.get("identity_service_name") }), 
            headers={
                "X-Access-Token": call.access_token,
                "Accept": "application/json", 
            }
        )
        
        return SecurityConfiguration.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="authentication/auth",
    function=auth,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=SecurityConfiguration,
    options={ "identity_service_name": str }
)