from dataclasses import dataclass

from ......service.http_service import HTTPService
from ......model.private.http.joc.joc_v_2_6_5 import Authentication

@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    

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
