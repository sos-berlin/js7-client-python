from typing import Optional

from ......model.private.http.joc.joc_v_2_8_2 import Authentication
from ......model.private.api.endpoint import EndpointCall, EndpointDefinition


def login(call: EndpointCall) -> Authentication:
    basic_auth: Optional[str] = None
    
    if call.options:
        if call.options.get("basic_auth"):
            basic_auth = call.options.get("basic_auth")
    
    headers = {"Accept": "application/json"}
    
    if basic_auth:
        headers["Authorization"] = basic_auth
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/authentication/login", 
            body=None, 
            headers=headers
        )
        
        return Authentication.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="authentication/login",
    function=login,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Authentication,
    options={ "basic_auth": Optional[str] }
)