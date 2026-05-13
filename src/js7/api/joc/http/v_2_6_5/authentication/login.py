from dataclasses import dataclass
from typing import Optional, TypedDict

from ......service.http_service import HTTPService
from ......model.private.http.joc.joc_v_2_6_5 import Authentication


class Options(TypedDict):
    basic_auth: Optional[str]

@dataclass
class EndpointCall:
    http_service: HTTPService
    options: Options
    

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