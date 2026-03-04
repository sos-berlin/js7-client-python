from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import DraftConfiguration, DeployConfiguration, ReleaseConfiguration
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2, 
    OK as OK_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    PublishConfiguration as Configuration_V_2_8_2,
    CopyToFilter as CopyToFilter_V_2_8_2,
    Configurations as Configurations_V_2_8_2,
    Config as Config_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_repository_configuration_action(
    *,
    context: Context,
    controller_id: str,
    category: Literal["LOCAL", "ROLLOUT"], 
    configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            category=category,
            configurations=configurations,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/store", call=EndpointCall(
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
    controller_id: str,
    category: Literal["LOCAL", "ROLLOUT"], 
    configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]],
    audit_log: Optional[AuditLog]
) -> CopyToFilter_V_2_8_2:
    
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
    res_configuration = Configurations_V_2_8_2(
        draft_configurations=[
            Config_V_2_8_2(configuration=Configuration_V_2_8_2(
                commit_id=None,
                object_type=ConfigurationType_V_2_8_2(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, DraftConfiguration)
        ],
        
        deploy_configurations=[
            Config_V_2_8_2(configuration=Configuration_V_2_8_2(
                commit_id=c.commit_id,
                object_type=ConfigurationType_V_2_8_2(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, DeployConfiguration)
        ],
        
        released_configurations=[
            Config_V_2_8_2(configuration=Configuration_V_2_8_2(
                commit_id=None,
                object_type=ConfigurationType_V_2_8_2(c.object_type.value),
                path=c.path,
                recursive=c.recursive
            ))
            for c in configurations
            if isinstance(c, ReleaseConfiguration)
        ]
    )

    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return CopyToFilter_V_2_8_2(
        controller_id=controller_id,
        local=res_configuration if category == "LOCAL" else None,
        rollout=res_configuration if category == "ROLLOUT" else None,
        audit_log=res_audit_log,
    )