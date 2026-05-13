from typing import Literal, Optional

from ...context import Context
from ....api.joc.http.v_2_6_5.joc.cluster.run import run, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    ClusterServices as ClusterServices_V_2_6_5,
    ClusterServiceRun as ClusterServiceRun_V_2_6_5
)


def run_service_action(
    *, 
    context: Context,
    service_type: Literal["cleanup", "dailyplan"],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            service_type=service_type, 
            audit_log=audit_log
        )

        result = run(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        if not result.state:
            return False
        
        if result.state.value in ["ERROR", "MISSING_CONFIGURATION", "MISSING_HANDLERS", "MISSING_LICENSE", "UNCOMPLETED"]:
            raise Exception(f"Restart of service: {service_type} failed with state: {result.state.value}.")
        
        return True
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    service_type: Literal["cleanup", "dailyplan"], 
    audit_log: Optional[AuditLog]
) -> ClusterServiceRun_V_2_6_5:
    
    # Validate: service_type
    svc_types = ["cleanup", "dailyplan"]
    if not service_type:
        raise ValueError("'service_type' is required")
    if service_type not in svc_types:
        raise ValueError(f"Unsupported 'service_type': {service_type}. Supported values are: {svc_types}")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return ClusterServiceRun_V_2_6_5(
        type=ClusterServices_V_2_6_5(service_type), # Raises ValueError if invalid.
        audit_log=res_audit_log
    )