from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.controller import Controller
from ....api.joc.http.v_2_6_5.controller.register import register, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    RegisterParameters as RegisterParameters_V_2_6_5,
    RegisterParameter as RegisterParameter_V_2_6_5,
    ControllerRole as ControllerRole_V_2_6_5
)


def register_controller_action(
    *, 
    context: Context,
    controller_id: Optional[str],
    controllers: List[Controller],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            controllers=controllers,
            audit_log=audit_log
        )

        result = register(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: Optional[str],
    controllers: List[Controller],
    audit_log: Optional[AuditLog]
) -> RegisterParameters_V_2_6_5:

    # Validate: controllers
    for c in controllers:
        if not c.url:
            raise ValueError("Each controller must define a 'url'.")
        if c.role not in ["STANDALONE", "PRIMARY", "BACKUP"]:
            raise ValueError(f"Invalid controller role '{c.role}'. Expected one of: STANDALONE, PRIMARY, BACKUP.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return RegisterParameters_V_2_6_5(
        controller_id=controller_id,
        controllers=[
            RegisterParameter_V_2_6_5(
                url=c.url,
                cluster_url=c.cluster_url,
                role=ControllerRole_V_2_6_5(c.role), # Raises ValueError() if invalid.
                title=c.title,
            )
            for c in controllers
        ],
        audit_log=res_audit_log
    )