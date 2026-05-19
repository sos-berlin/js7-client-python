from typing import Any, Dict, Literal, Optional

from ...context import Context
from ....api.joc.http.v_2_6_5.note.post.add import add, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_6_5 import (
    CommonConfigurationType as CommonConfigurationType_V_2_6_5,
    AddPost as AddPost_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5,
    Severity as Severity_V_2_6_5
)


def post_to_note_action(
    *,
    context: Context,
    name: str,
    object_type: ObjectType,
    content: str,
    severity: Literal["INFO", "LOW", "NORMAL", "HIGH", "CRITICAL"],
    audit_log: Optional[AuditLog]
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            name=name,
            object_type=object_type,
            content=content,
            severity=severity,
            audit_log=audit_log
        )

        result = add(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))

        return result.model_dump(mode="json").get("posts") or {}
        
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    name: str,
    object_type: ObjectType,
    content: str,
    severity: Literal["INFO", "LOW", "NORMAL", "HIGH", "CRITICAL"],
    audit_log: Optional[AuditLog]
) -> AddPost_V_2_6_5:

    # Validate: name
    if not name:
        raise ValueError("'name' is required.")
    
    # Validate: content
    if not content:
        raise ValueError("'content' is required.")
    
    # Validate: severity
    if severity not in ("INFO", "LOW", "NORMAL", "HIGH", "CRITICAL"):
        raise ValueError("'severity' must be 'INFO', 'LOW', 'NORMAL', 'HIGH' or 'CRITICAL'.")
    
    # Build: audit_log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return AddPost_V_2_6_5(
        name=name,
        object_type=CommonConfigurationType_V_2_6_5(object_type.value), # Raises ValueError() if invalid.
        content=content,
        severity=Severity_V_2_6_5(severity), # Raises ValueError() if invalid.
        audit_log=res_audit_log
    )
