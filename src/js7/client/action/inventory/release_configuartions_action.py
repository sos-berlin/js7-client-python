from typing import List, Optional

from ....model.public.client.common.configurations import ReleaseConfiguration
from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    CommonRequestFilter as CommonRequestFilter_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    ReleaseFilter as ReleaseFilter_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def release_configuartions_action(
    *,
    context: Context,
    update: Optional[List[ReleaseConfiguration]],
    delete: Optional[List[ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            update=update,
            delete=delete,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/release", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, 
    update: Optional[List[ReleaseConfiguration]],
    delete: Optional[List[ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> ReleaseFilter_V_2_8_2:
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: Update
    res_update = [
        CommonRequestFilter_V_2_8_2(
            path=u.path,
            object_type=ConfigurationType_V_2_8_2(u.object_type.value) # Raises ValueError() if invalid.
        )
        for u in update
    ] if update else None
    
    # Build: Delete
    res_delete = [
        CommonRequestFilter_V_2_8_2(
            path=d.path,
            object_type=ConfigurationType_V_2_8_2(d.object_type.value) # Raises ValueError() if invalid.
        )
        for d in delete
    ] if delete else None
    
    # Result
    return ReleaseFilter_V_2_8_2(
        audit_log=res_audit_log,
        delete=res_delete,
        update=res_update,
        add_orders_date_from=None, 
        include_late=None,         
    )