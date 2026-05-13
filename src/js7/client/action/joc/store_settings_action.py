import json
from typing import Any, Dict, Optional

from ...context import Context
from ....api.joc.http.v_2_6_5.settings.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_6_5 import (
    StoreSettingsFilter as StoreSettingsFilter_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def store_settings_action(*, context: Context, payload: Dict[str, Any], audit_log: Optional[AuditLog]) -> bool:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            payload=payload,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    payload: Dict[str, Any],
    audit_log: Optional[AuditLog]
) -> StoreSettingsFilter_V_2_6_5:

    # Validate: payload
    if not payload:
        raise ValueError("'payload' is required")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return StoreSettingsFilter_V_2_6_5(
        configuration_item=json.dumps(payload),
        audit_log=res_audit_log
    )