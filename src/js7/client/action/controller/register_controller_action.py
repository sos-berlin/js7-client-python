from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.controller import Controller
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    RegisterParameters as RegisterParameters_V_2_8_2,
    RegisterParameter as RegisterParameter_V_2_8_2,
    ControllerRole as ControllerRole_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def register_controller_action(
    *, 
    context: Context,
    controller_id: Optional[str],
    controllers: List[Controller],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            controllers=controllers,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="controller/register", call=EndpointCall(
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
def _build_v_2_8_2_request(
    *, 
    controller_id: Optional[str],
    controllers: List[Controller],
    audit_log: Optional[AuditLog]
) -> RegisterParameters_V_2_8_2:

    # Validate: controllers
    for c in controllers:
        if not c.url:
            raise ValueError("Each controller must define a 'url'.")
        if c.role not in ["STANDALONE", "PRIMARY", "BACKUP"]:
            raise ValueError(f"Invalid controller role '{c.role}'. Expected one of: STANDALONE, PRIMARY, BACKUP.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return RegisterParameters_V_2_8_2(
        controller_id=controller_id,
        controllers=[
            RegisterParameter_V_2_8_2(
                url=c.url,
                cluster_url=c.cluster_url,
                role=ControllerRole_V_2_8_2(c.role), # Raises ValueError() if invalid.
                title=c.title,
            )
            for c in controllers
        ],
        audit_log=res_audit_log
    )