from .......model.private.api.endpoint import EndpointCall, EndpointDefinition
from .......model.private.http.joc.joc_v_2_8_2 import RoleListFilter, Roles


def role(call: EndpointCall) -> Roles:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, RoleListFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.RoleListFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/iam/roles", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Roles.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="iam/roles",
    function=role,
    version=("2.6.5", "2.8.3"),
    payload_model=RoleListFilter,
    response_model=Roles,
    options=None
)