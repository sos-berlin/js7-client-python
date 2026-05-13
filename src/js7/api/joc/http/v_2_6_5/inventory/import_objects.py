from typing import Dict, Optional, TypedDict
from dataclasses import dataclass

from ......service.http_service import HTTPService
from ......model.private.http.joc.joc_v_2_6_5 import OK


class Options(TypedDict):
    format:                str
    overwrite:             bool
    target_folder:         Optional[str]
    suffix:                Optional[str]
    prefix:                Optional[str]
    overwrite_tags:        Optional[bool]
    audit_log_ticket_link: Optional[str]
    audit_log_comment:     Optional[str]
    audit_log_time_spent:  Optional[str]


@dataclass
class EndpointCall:
    http_service: HTTPService
    access_token: str
    payload:      bytes
    options:      Options
    

def import_objects(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options:
        raise ValueError("'options' is required in function call.")
    
    if not isinstance(call.payload, bytes):
        raise ValueError("'payload' is not of type bytes.")
    
    format = call.options.get("format")
    overwrite = call.options.get("overwrite")
    target_folder = call.options.get("target_folder")
    suffix = call.options.get("suffix")
    prefix = call.options.get("prefix")
    overwrite_tags = call.options.get("overwrite_tags")
    audit_log_ticket_link = call.options.get("audit_log_ticket_link")
    audit_log_comment = call.options.get("audit_log_comment")
    audit_log_time_spent = call.options.get("audit_log_time_spent")
    
    if not format:
        raise ValueError("'format' is required in options.")
    
    if format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'format' must be 'ZIP' or 'TAR_GZ'.")
            
    form_fields: Dict[str, str] = {
        "overwrite": str(overwrite).lower(),
        "format": str(format)
    }
    
    if target_folder:
        form_fields["targetFolder"] = target_folder
    
    if suffix:
        form_fields["suffix"] = suffix
        
    if prefix:
        form_fields["prefix"] = prefix
        
    if overwrite_tags:
        form_fields["overwriteTags"] = str(overwrite_tags).lower()
        
    if audit_log_ticket_link:
        form_fields["ticketLink"] = audit_log_ticket_link
    if audit_log_comment:
        form_fields["comment"] = audit_log_comment
    if audit_log_time_spent:
        form_fields["timeSpent"] = audit_log_time_spent
    
    with call.http_service as http:
        resp = http.upload_file(
            path="/joc/api/inventory/import", 
            access_token=call.access_token,
            file=call.payload,
            filename="import.zip" if format == "ZIP" else "import.tar.gz",
            form_fields=form_fields
        )
        
        return OK.model_validate_json(resp)
