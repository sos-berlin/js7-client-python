from .......model.private.http.joc.joc_v_2_8_2 import ExportFilter
from .......model.private.api.endpoint import EndpointCall, EndpointDefinition


def export(call: EndpointCall) -> bytes:    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, ExportFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.ExportFilter.")
    
    if not call.access_token:
        raise ValueError("'access_token' ist required in function call")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/export",
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/octet-stream"
            }
        )
        
        return resp
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/export",
    function=export,
    version=("2.6.5", "2.8.3"),
    payload_model=ExportFilter,
    response_model=bytes,
    options=None
)
