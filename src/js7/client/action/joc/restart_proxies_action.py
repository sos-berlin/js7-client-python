from typing import Optional

from js7.model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    ClusterRestart as ClusterRestart_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def restart_proxies_action(*, context: Context, audit_log: Optional[AuditLog]) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(audit_log=audit_log)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="joc/proxies/restart", call=EndpointCall(
        http_service=context.http_service,
        payload=request_data,
        access_token=context.auth_provider.login(),
        options=None
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, audit_log: Optional[AuditLog]) -> ClusterRestart_V_2_8_2:
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ClusterRestart_V_2_8_2(
        type=None,
        audit_log=res_audit_log
    )