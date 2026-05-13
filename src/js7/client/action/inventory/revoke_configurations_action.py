from typing import List, Optional

from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.deployment.revoke import revoke, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.configurations import DeployConfiguration
from ....model.private.http.joc.joc_v_2_6_5 import (
    Config as Config_V_2_6_5,
    PublishConfiguration as Configuration_V_2_6_5,
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5,
    RevokeFilter as RevokeFilter_V_2_6_5
)


def revoke_configurations_action(
    *, 
    context: Context, 
    controller_ids: List[str], 
    configurations: List[DeployConfiguration], 
    audit_log: Optional[AuditLog]
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_ids=controller_ids, 
            configurations=configurations, 
            audit_log=audit_log
        )

        result = revoke(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_ids: List[str], 
    configurations: List[DeployConfiguration], 
    audit_log: Optional[AuditLog]
) -> RevokeFilter_V_2_6_5:
    
    # Build: Audit log
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    if not configurations:
        raise ValueError("At least one entry is required in 'deploy_configurations'.")
    
    # Build: res_configs
    res_configs = [
        Config_V_2_6_5(configuration=Configuration_V_2_6_5(
            commit_id=c.commit_id,
            path=c.path,
            recursive=c.recursive,
            object_type=ConfigurationType_V_2_6_5(c.object_type), # Raises ValueError() if invalid
        ))
        for c in configurations
    ]
    
    # Result
    return RevokeFilter_V_2_6_5(
        audit_log=res_audit_log,
        controller_ids=controller_ids,
        deploy_configurations=res_configs,
        cancel_orders_date_from=None, # Wrong domain
    )