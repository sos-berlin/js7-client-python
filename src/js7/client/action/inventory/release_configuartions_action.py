from typing import List, Optional

from ....model.public.client.common.configurations import ReleaseConfiguration
from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.release import release, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    CommonRequestFilter as CommonRequestFilter_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5,
    ReleaseFilter as ReleaseFilter_V_2_6_5
)


def release_configuartions_action(
    *,
    context: Context,
    update: Optional[List[ReleaseConfiguration]],
    delete: Optional[List[ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            update=update,
            delete=delete,
            audit_log=audit_log
        )

        result = release(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, 
    update: Optional[List[ReleaseConfiguration]],
    delete: Optional[List[ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> ReleaseFilter_V_2_6_5:
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: Update
    res_update = [
        CommonRequestFilter_V_2_6_5(
            path=u.path,
            object_type=ConfigurationType_V_2_6_5(u.object_type.value) # Raises ValueError() if invalid.
        )
        for u in update
    ] if update else None
    
    # Build: Delete
    res_delete = [
        CommonRequestFilter_V_2_6_5(
            path=d.path,
            object_type=ConfigurationType_V_2_6_5(d.object_type.value) # Raises ValueError() if invalid.
        )
        for d in delete
    ] if delete else None
    
    # Result
    return ReleaseFilter_V_2_6_5(
        audit_log=res_audit_log,
        delete=res_delete,
        update=res_update,
        add_orders_date_from=None, 
        include_late=None,         
    )