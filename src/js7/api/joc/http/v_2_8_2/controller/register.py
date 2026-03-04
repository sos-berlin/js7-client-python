from datetime import datetime, timezone

from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import RegisterParameters, OK


def register(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, RegisterParameters):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.RegisterParameters.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/controller/register", 
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
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="controller/register",
    function=register,
    version=("2.6.5", "2.8.3"),
    payload_model=RegisterParameters,
    response_model=OK,
    options=None
)