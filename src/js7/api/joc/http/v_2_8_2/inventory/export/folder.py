from .......model.private.api.endpoint import EndpointCall, EndpointDefinition
from .......model.private.http.joc.joc_v_2_8_2 import ExportFolderFilter


def folder(call: EndpointCall) -> bytes:
    if not call.access_token:
        raise ValueError("'access_token' ist required in function call.")

    if not call.payload:
        raise ValueError("'payload' is required in function call.")

    if not isinstance(call.payload, ExportFolderFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.ExportFolderFilter.")

    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/export/folder",
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/octet-stream"
            }
        )
        
        return resp

ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/export/folder",
    function=folder,
    version=("2.6.5", "2.8.3"),
    payload_model=ExportFolderFilter,
    response_model=bytes,
    options=None
)