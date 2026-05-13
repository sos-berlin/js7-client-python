import json
from typing import Any, Dict, TypedDict
from dataclasses import dataclass

from ......service.http_service import HTTPService
from ......model.private.http.joc.joc_v_2_6_5 import Validate
from ......model.public.client.enum.object_types import ObjectType

class Options(TypedDict):
    object_type: ObjectType


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      Dict[str, Any]
    options:      Options


def validate(call: EndpointCall) -> Validate:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options or not call.options.get("object_type"):
        raise ValueError("'options' is required in function call.")
    
    object_type = call.options.get("object_type")
    if not object_type:
        raise ValueError("'object_type' in options is required.")
    
    with call.http_service as http:
        resp = http.post(
            path=f"/joc/api/inventory/{object_type.value}/validate", 
            body=json.dumps(call.payload),
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Validate.model_validate_json(resp)
