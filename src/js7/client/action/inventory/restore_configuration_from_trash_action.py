from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.inventory.trash.restore import restore, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.configurations import Configuration
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    RestoreRequestFilter as RestoreRequestFilter_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5
)


# Returns: new configuration path
def restore_configuration_from_trash_action(
    *, 
    context: Context, 
    configuration: Configuration,
    new_path: str,
    add_prefix: Optional[str],
    add_suffix: Optional[str],
    audit_log: Optional[AuditLog]
) -> str:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            configuration=configuration,
            new_path=new_path,
            add_prefix=add_prefix,
            add_suffix=add_suffix,
            audit_log=audit_log
        )

        result = restore(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result.path or ""
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    configuration: Configuration,
    new_path: str,
    add_prefix: Optional[str],
    add_suffix: Optional[str],
    audit_log: Optional[AuditLog]
) -> RestoreRequestFilter_V_2_6_5:

    # Validate: new_path
    if not new_path:
        raise ValueError("'new_path' is required.")
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return RestoreRequestFilter_V_2_6_5(
        path=configuration.path,
        object_type=ConfigurationType_V_2_6_5(configuration.object_type.value), # Raises ValueError() if invalid.
        new_path=new_path,
        prefix=add_prefix,
        suffix=add_suffix,
        audit_log=res_audit_log,
    )