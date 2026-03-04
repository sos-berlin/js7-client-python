from typing import Literal, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
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
    url: str,
    cluster_url: Optional[str],
    role: Literal["STANDALONE", "PRIMARY", "BACKUP"],
    title: Optional[str],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            url=url,
            cluster_url=cluster_url,
            role=role,
            title=title,
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
    url: str,
    cluster_url: Optional[str],
    role: Literal["STANDALONE", "PRIMARY", "BACKUP"],
    title: Optional[str],
    audit_log: Optional[AuditLog]
) -> RegisterParameters_V_2_8_2:

    # Validate: url
    if not url:
        raise ValueError("'url' is required.")
    
    # Validate: role
    if role not in ["STANDALONE", "PRIMARY", "BACKUP"]:
        raise ValueError(f"Invalid 'role': {role}.")
    
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
                url=url,
                cluster_url=cluster_url,
                role=ControllerRole_V_2_8_2(role), # Raises ValueError() if invalid.
                title=title,
            )
        ],
        audit_log=res_audit_log
    )