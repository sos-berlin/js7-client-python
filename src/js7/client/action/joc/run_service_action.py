from typing import Literal, Optional

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    ClusterServices as ClusterServices_V_2_8_2,
    ClusterResponse as ClusterResponse_V_2_8_2,
    ClusterServiceRun as ClusterServiceRun_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def run_service_action(
    *, 
    context: Context,
    service_type: Literal["cleanup", "cluster", "dailyplan", "history", "lognotification", "monitor"],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(service_type=service_type, audit_log=audit_log)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="joc/cluster/run", call=EndpointCall(
        http_service=context.http_service,
        payload=request_data,
        access_token=context.auth_provider.login(),
        options=None
    ))
    
    if isinstance(result, ClusterResponse_V_2_8_2):
        if not result.state:
            return False
        
        if result.state.value in ["ERROR", "MISSING_CONFIGURATION", "MISSING_HANDLERS", "MISSING_LICENSE", "UNCOMPLETED"]:
            raise Exception(f"Restart of service: {service_type} failed with state: {result.state.value}.")
        
        return True
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    service_type: Literal["cleanup", "cluster", "dailyplan", "history", "lognotification", "monitor"], 
    audit_log: Optional[AuditLog]
) -> ClusterServiceRun_V_2_8_2:
    
    # Validate: service_type
    svc_types = ["cleanup", "cluster", "dailyplan", "history", "lognotification", "monitor"]
    if not service_type:
        raise ValueError("'service_type' is required")
    if service_type not in svc_types:
        raise ValueError(f"Unsupported 'service_type': {service_type}. Supported values are: {svc_types}")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ClusterServiceRun_V_2_8_2(
        type=ClusterServices_V_2_8_2(service_type), # Raises ValueError if invalid.
        audit_log=res_audit_log
    )