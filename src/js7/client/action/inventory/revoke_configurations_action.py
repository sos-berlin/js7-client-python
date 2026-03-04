from typing import List, Optional

from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.configurations import DeployConfiguration
from ....model.private.http.joc.joc_v_2_8_2 import (
    Config as Config_V_2_8_2,
    PublishConfiguration as Configuration_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    RevokeFilter as RevokeFilter_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def revoke_configurations_action(
    *, 
    context: Context, 
    controller_ids: List[str], 
    configurations: List[DeployConfiguration], 
    audit_log: Optional[AuditLog]
) -> bool:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_ids=controller_ids, 
            configurations=configurations, 
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/deployment/revoke", call=EndpointCall(
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
    controller_ids: List[str], 
    configurations: List[DeployConfiguration], 
    audit_log: Optional[AuditLog]
) -> RevokeFilter_V_2_8_2:
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    if not configurations:
        raise ValueError("At least one entry is required in 'deploy_configurations'.")
    
    # Build: res_configs
    res_configs = [
        Config_V_2_8_2(configuration=Configuration_V_2_8_2(
            commit_id=c.commit_id,
            path=c.path,
            recursive=c.recursive,
            object_type=ConfigurationType_V_2_8_2(c.object_type), # Raises ValueError() if invalid
        ))
        for c in configurations
    ]
    
    # Result
    return RevokeFilter_V_2_8_2(
        audit_log=res_audit_log,
        controller_ids=controller_ids,
        deploy_configurations=res_configs,
        cancel_orders_date_from=None, # Wrong domain
    )