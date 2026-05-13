from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import Configuration
from ....api.joc.http.v_2_6_5.inventory.trash.delete.delete import delete, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5, 
    CommonRequestFilter as CommonRequestFilter_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    CommonRequestFilters as CommonRequestFilters_V_2_6_5
)


def remove_configurations_from_trash_action(
    *, 
    context: Context,
    configurations: List[Configuration],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            configurations=configurations,
            audit_log=audit_log
        )

        result = delete(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    configurations: List[Configuration],
    audit_log: Optional[AuditLog]
) -> CommonRequestFilters_V_2_6_5:
    
    # Validate: configurations
    if not configurations:
        raise ValueError("'configurations' are required.")
    
    # Build: res_objects
    res_objects = [
        CommonRequestFilter_V_2_6_5(
            path=c.path,
            object_type=ConfigurationType_V_2_6_5(c.object_type.value) # Raises ValueError() if invalid.
        )
        for c in configurations
    ]
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return CommonRequestFilters_V_2_6_5(
        objects=res_objects,
        audit_log=res_audit_log
    )