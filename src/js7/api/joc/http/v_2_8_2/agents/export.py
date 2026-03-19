from ......model.private.api.endpoint import EndpointCall, EndpointDefinition
from ......model.private.http.joc.joc_v_2_8_2 import AgentExportFilter


def export(call: EndpointCall) -> bytes:    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not call.access_token:
        raise ValueError("'access_token' ist required in function call")
    
    if not isinstance(call.payload, AgentExportFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.AgentExportFilter.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/agents/export",
            body=body,
            headers={
                "X-Access-Token": call.access_token
            }
        )
        
        return resp
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="agents/export",
    function=export,
    version=("2.6.5", "2.8.3"),
    payload_model=AgentExportFilter,
    response_model=bytes,
    options=None
)
