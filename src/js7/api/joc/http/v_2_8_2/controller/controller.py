from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import URLParameter, JobScheduler200


def controller(call: EndpointCall) -> JobScheduler200:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, URLParameter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.URLParameter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/controller", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return JobScheduler200.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="controller",
    function=controller,
    version=("2.6.5", "2.8.3"),
    payload_model=URLParameter,
    response_model=JobScheduler200,
    options=None
)