from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.configurations import Configuration
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    RequestFilter as RequestFilter_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    ResponseNewPath as ResponseNewPath_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


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
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            configuration=configuration,
            new_path=new_path,
            add_prefix=add_prefix,
            add_suffix=add_suffix,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/trash/restore", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, ResponseNewPath_V_2_8_2):
        if result.path:
            return result.path
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *, 
    configuration: Configuration,
    new_path: str,
    add_prefix: Optional[str],
    add_suffix: Optional[str],
    audit_log: Optional[AuditLog]
) -> RequestFilter_V_2_8_2:

    # Validate: new_path
    if not new_path:
        raise ValueError("'new_path' is required.")
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return RequestFilter_V_2_8_2(
        path=configuration.path,
        object_type=ConfigurationType_V_2_8_2(configuration.object_type.value), # Raises ValueError() if invalid.
        new_path=new_path,
        prefix=add_prefix,
        suffix=add_suffix,
        audit_log=res_audit_log,
    )