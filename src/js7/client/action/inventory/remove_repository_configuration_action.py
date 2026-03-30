from typing import List, Literal, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import Configuration
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2, 
    OK as OK_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    DeleteFromFilter as DeleteFromFilter_V_2_8_2,
    Category as Category_V_2_8_2,
    PublishConfiguration as PublishConfiguration_V_2_8_2,
    PublishConfig as PublishConfig_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def remove_repository_configuration_action(
    *, 
    context: Context, 
    configurations: List[Configuration],
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(configurations=configurations, category=category, audit_log=audit_log)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/delete", call=EndpointCall(
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
    configurations: List[Configuration],
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog]
) -> DeleteFromFilter_V_2_8_2:
    
    # Validates configurations
    if not configurations:
        raise ValueError("At least one configuration in 'configurations' is required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Build: Configurations
    res_configurations: List[PublishConfiguration_V_2_8_2] = [
        PublishConfiguration_V_2_8_2(
            object_type=ConfigurationType_V_2_8_2(c.object_type.value), # Raises ValueError() if invalid.
            path=c.path,
        )
        for c in configurations
    ]

    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return DeleteFromFilter_V_2_8_2(
        configurations=[
            PublishConfig_V_2_8_2(configuration=c)
            for c in res_configurations
        ],
        category=Category_V_2_8_2(category), # Raises ValueError() if invalid.
        audit_log=res_audit_log,
    )