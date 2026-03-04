from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import WorkflowsFilter, Workflows


def workflows(call: EndpointCall) -> Workflows:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, WorkflowsFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.WorkflowsFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/workflows", 
            body=body,
            headers={
                "X-Access-Token": call.access_token,
                "Accept": "application/json"
            }
        )
        
        return Workflows.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="workflows",
    function=workflows,
    version=("2.6.5", "2.8.3"),
    payload_model=WorkflowsFilter,
    response_model=Workflows,
    options=None
)
