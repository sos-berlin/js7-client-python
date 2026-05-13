from dataclasses import dataclass

from .......service.http_service import HTTPService
from .......model.private.http.joc.joc_v_2_6_5 import ExportFolderFilter


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      ExportFolderFilter
    
    
def folder(call: EndpointCall) -> bytes:
    if not call.access_token:
        raise ValueError("'access_token' ist required in function call.")

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
