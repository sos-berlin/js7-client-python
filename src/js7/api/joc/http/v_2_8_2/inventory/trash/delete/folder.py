from ........model.private.http.joc.joc_v_2_8_2 import CommonRequestFolder, OK
from ........model.private.api.endpoint import EndpointCall, EndpointDefinition


def folder(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, CommonRequestFolder):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.CommonRequestFolder.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/inventory/trash/delete/folder", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return OK.model_validate_json(resp)

ENDPOINT_DEFINITION = EndpointDefinition(
    id="inventory/trash/delete/folder",
    function=folder,
    version=("2.6.5", "2.8.3"),
    payload_model=CommonRequestFolder,
    response_model=OK,
    options=None
)