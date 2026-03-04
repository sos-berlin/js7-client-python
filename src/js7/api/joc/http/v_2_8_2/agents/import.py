from typing import Dict, Optional

from ......model.private.api.endpoint import EndpointCall, EndpointDefinition
from ......model.private.http.joc.joc_v_2_8_2 import OK


def import_(call: EndpointCall) -> OK:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.options:
        raise ValueError("'options' is required in function call.")
    
    if not isinstance(call.payload, bytes):
        raise ValueError("'payload' is not of type bytes.")
    
    format = call.options.get("format")
    controller_id = call.options.get("controller_id")
    overwrite = call.options.get("overwrite")
    audit_log_ticket_link = call.options.get("audit_log_ticket_link")
    audit_log_comment = call.options.get("audit_log_comment")
    audit_log_time_spent = call.options.get("audit_log_time_spent")
    
    if not controller_id:
        raise ValueError("'controller_id' is required in options.")
    
    if overwrite is None:
        raise ValueError("'overwrite' is required in options.")
    
    if not format:
        raise ValueError("'format' is required in options.")
    
    if format not in ("ZIP", "TAR_GZ"):
        raise ValueError("'format' must be 'ZIP' or 'TAR_GZ'.")
    
    form_fields: Dict[str, str] = {
        "format": str(format),
        "overwrite": str(overwrite).lower(),
        "controllerId": str(controller_id),
    }
    
    if audit_log_ticket_link:
        form_fields["ticketLink"] = audit_log_ticket_link
    if audit_log_comment:
        form_fields["comment"] = audit_log_comment
    if audit_log_time_spent:
        form_fields["timeSpent"] = audit_log_time_spent
    
    with call.http_service as http:
        resp = http.upload_file(
            path="/joc/api/agents/import", 
            access_token=call.access_token,
            file=call.payload,
            filename="import.zip" if format == "ZIP" else "import.tar.gz",
            form_fields=form_fields
        )
        
        return OK.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="agents/import",
    function=import_,
    version=("2.6.5", "2.8.3"),
    payload_model=bytes,
    response_model=OK,
    options={
        "format": str,
        "overwrite": bool,
        "controller_id": str,
        "audit_log_ticket_link": Optional[str],
        "audit_log_comment": Optional[str],
        "audit_log_time_spent": Optional[str]
    }
)