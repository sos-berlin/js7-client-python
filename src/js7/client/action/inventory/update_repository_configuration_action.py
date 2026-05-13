from typing import List, Literal, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import Configuration
from ....api.joc.http.v_2_6_5.inventory.repository.update import update, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    Category as Category_V_2_6_5,
    PublishConfiguration as Configuration_V_2_6_5,
    UpdateFromFilter as UpdateFromFilter_V_2_6_5,
    Config as Config_V_2_6_5
)


def update_repository_configuration_action(
    *, 
    context: Context, 
    configurations: List[Configuration],
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            configurations=configurations, 
            category=category, 
            audit_log=audit_log
        )

        result = update(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    configurations: List[Configuration],
    category: Literal["LOCAL", "ROLLOUT"],
    audit_log: Optional[AuditLog]
) -> UpdateFromFilter_V_2_6_5:
    
    # Validates configurations
    if not configurations:
        raise ValueError("At least one configuration in 'Configurations' is required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Build: Configurations
    res_configurations = [
        Config_V_2_6_5(configuration=Configuration_V_2_6_5(
            object_type=ConfigurationType_V_2_6_5(c.object_type.value), # Raises ValueError() if invalid.
            path=c.path
        ))
        for c in configurations
    ]

    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return UpdateFromFilter_V_2_6_5(
        configurations=res_configurations,
        category=Category_V_2_6_5(category), # Raises ValueError() if invalid.
        audit_log=res_audit_log,
    )