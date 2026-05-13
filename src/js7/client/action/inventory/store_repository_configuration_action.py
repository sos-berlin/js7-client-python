from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import DraftConfiguration, DeployConfiguration, ReleaseConfiguration
from ....api.joc.http.v_2_6_5.inventory.repository.store import store, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    PublishConfiguration as Configuration_V_2_6_5,
    CopyToFilter as CopyToFilter_V_2_6_5,
    Configurations as Configurations_V_2_6_5,
    Config as Config_V_2_6_5
)


def store_repository_configuration_action(
    *,
    context: Context,
    controller_id: str,
    category: Literal["LOCAL", "ROLLOUT"], 
    configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            category=category,
            configurations=configurations,
            audit_log=audit_log
        )

        result = store(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    category: Literal["LOCAL", "ROLLOUT"], 
    configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> CopyToFilter_V_2_6_5:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Validates configurations
    if not configurations:
        raise ValueError("At least one configuration in 'configurations' is required.")
    
    # Build: Configuration
    res_configuration = Configurations_V_2_6_5(
        draft_configurations=[
            Config_V_2_6_5(configuration=Configuration_V_2_6_5(
                commit_id=None,
                object_type=ConfigurationType_V_2_6_5(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, DraftConfiguration)
        ],
        
        deploy_configurations=[
            Config_V_2_6_5(configuration=Configuration_V_2_6_5(
                commit_id=c.commit_id,
                object_type=ConfigurationType_V_2_6_5(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, DeployConfiguration)
        ],
        
        released_configurations=[
            Config_V_2_6_5(configuration=Configuration_V_2_6_5(
                commit_id=None,
                object_type=ConfigurationType_V_2_6_5(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, ReleaseConfiguration)
        ]
    )

    # Build: Audit Log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return CopyToFilter_V_2_6_5(
        controller_id=controller_id,
        local=res_configuration if category == "LOCAL" else None,
        rollout=res_configuration if category == "ROLLOUT" else None,
        audit_log=res_audit_log,
    )