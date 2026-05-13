from dataclasses import dataclass

from .......service.http_service import HTTPService
from .......model.private.http.joc.joc_v_2_6_5 import AccountNamesFilter, OK


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      AccountNamesFilter
    

def reset_password(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/iam/accounts/resetpassword", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return OK.model_validate_json(resp)
