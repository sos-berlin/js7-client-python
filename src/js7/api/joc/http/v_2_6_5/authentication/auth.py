import json
from typing import TypedDict
from dataclasses import dataclass

from ......service.http_service import HTTPService
from ......model.private.http.joc.joc_v_2_6_5 import SecurityConfiguration


class Options(TypedDict):
    identity_service_name: str


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    options: Options
    

def auth(call: EndpointCall) -> SecurityConfiguration:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options or not call.options.get("identity_service_name"):
        raise ValueError("'identity_service_name' is required in function call.")
    
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
