from datetime import datetime, timezone
from dataclasses import dataclass

from .......service.http_service import HTTPService
from .......model.private.http.joc.joc_v_2_6_5 import IdentityService, OK


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      IdentityService
    

def store(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/iam/identityservice/store", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        # Patch: The status code is validated in the validator: ./js7/validator/http/joc_http_status_validator.py
        now = datetime.now(timezone.utc)
        if not resp:
            return OK(delivery_date=now, ok=False)
        return OK(delivery_date=now, ok=True)
