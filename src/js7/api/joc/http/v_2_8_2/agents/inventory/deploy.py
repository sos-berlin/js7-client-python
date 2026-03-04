from .......model.private.api.endpoint import EndpointDefinition, EndpointCall
from .......model.private.http.joc.joc_v_2_8_2 import DeployAgents, OK


def deploy(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, DeployAgents):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.DeployAgents.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/agents/inventory/deploy", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return OK.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="agents/inventory/deploy",
    function=deploy,
    version=("2.6.5", "2.8.3"),
    payload_model=DeployAgents,
    response_model=OK,
    options=None
)