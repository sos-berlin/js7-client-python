from typing import Dict, Literal, Optional, TypedDict
from dataclasses import dataclass

from .......service.http_service import HTTPService
from .......model.private.http.joc.joc_v_2_6_5 import OK


class Options(TypedDict):
    controller_id:         str
    signature_algorithm:   str
    format:                Literal["ZIP", "TAR_GZ"]
    audit_log_ticket_link: Optional[str]
    audit_log_comment:     Optional[str]
    audit_log_time_spent:  Optional[str]


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      bytes
    options:      Options
    

def import_deploy(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not call.options:
        raise ValueError("'options' is required in function call.")    
    
    controller_id = call.options.get("controller_id")
    signature_algorithm = call.options.get("signature_algorithm")
    audit_log_ticket_link = call.options.get("audit_log_ticket_link")
    audit_log_comment = call.options.get("audit_log_comment")
    audit_log_time_spent = call.options.get("audit_log_time_spent")
    format = call.options.get("format")
    
    if not controller_id:
        raise ValueError("'controller_id' is required in options.")
    
    if not signature_algorithm:
        raise ValueError("'signature_algorithm' is required in options.")
    
    form_fields: Dict[str, str] = {
        "format": format,
        "controllerId": controller_id,
        "signatureAlgorithm": signature_algorithm
    }
    
    if audit_log_ticket_link:
        form_fields["ticketLink"] = audit_log_ticket_link
    if audit_log_comment:
        form_fields["comment"] = audit_log_comment
    if audit_log_time_spent:
        form_fields["timeSpent"] = audit_log_time_spent
    
    with call.http_service as http:
        resp = http.upload_file(
            path="/joc/api/inventory/deployment/import_deploy", 
            access_token=call.access_token,
            file=call.payload,
            filename="import.zip",
            form_fields=form_fields
        )
        
        return OK.model_validate(resp)
