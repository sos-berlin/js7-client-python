import json
from typing import Dict
from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import Validate


def validate(call: EndpointCall) -> Validate:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options or not call.options.get("object_type"):
        raise ValueError("'options' is required in function call.")
    
    object_type = call.options.get("object_type")
    if not object_type:
        raise ValueError("'object_type' in options is required.")
    
    if not isinstance(call.payload, Dict):
        raise TypeError("'payload' is not a dictionary.")
    
    with call.http_service as http:
        resp = http.post(
            path=f"/joc/api/inventory/{object_type}/validate", 
            body=json.dumps(call.payload),
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Validate.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/validate",
    function=validate,
    version=("2.6.5", "2.8.3"),
    payload_model=Dict,
    response_model=Validate,
    options={
        "object_type": str,
    }
)