from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.configurations import DeployConfiguration, DraftConfiguration
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    DeployFilter as DeployFilter_V_2_8_2,
    OK as OK_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    DeployablesValidFilter as DeployablesValidFilter_V_2_8_2,
    Config as Config_V_2_8_2,
    PublishConfiguration as Configuration_V_2_8_2,
    CommonConfigurationType as ConfigurationType_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


# (i) Daily Plan operations such as add_orders_date_from should be executed in a separate function.
def deploy_configurations_action(
    *,
    context: Context,
    controller_id: str,
    delete_deployed_configs: Optional[List[DeployConfiguration]],
    deploy_draft_configs: Optional[List[DraftConfiguration]],
    redeploy_deployed_configs: Optional[List[DeployConfiguration]],
    audit_log: Optional[AuditLog]
) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            delete_deployed_configs=delete_deployed_configs,
            deploy_draft_configs=deploy_draft_configs,
            redeploy_deployed_configs=redeploy_deployed_configs,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/deployment/deploy", call=EndpointCall(
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
    delete_deployed_configs: Optional[List[DeployConfiguration]],
    deploy_draft_configs: Optional[List[DraftConfiguration]],
    redeploy_deployed_configs: Optional[List[DeployConfiguration]],
    audit_log: Optional[AuditLog]
) -> DeployFilter_V_2_8_2:

    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: any_of(delete_deployed_object, deploy_draft_object, redeploy_deployed_object)
    if not (delete_deployed_configs or deploy_draft_configs or redeploy_deployed_configs):
        raise ValueError("Any of 'delete_deployed_configs, deploy_draft_configs, redeploy_deployed_configs' must be set.")
    
    # Build: audit_log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Build: delete_deployed_object
    res_delete: Optional[DeployablesValidFilter_V_2_8_2] = None
    if delete_deployed_configs:
        res_delete = DeployablesValidFilter_V_2_8_2(
            deploy_configurations=[
                Config_V_2_8_2(
                    configuration=Configuration_V_2_8_2(
                        commit_id=c.commit_id,
                        object_type=ConfigurationType_V_2_8_2(c.object_type), # Raises ValueErro() if invalid.
                        path=c.path,
                        recursive=c.recursive,
                    )
                )
                for c in delete_deployed_configs
            ]
        )
    
    # Build: Store
    store_draft_configs: Optional[List[Config_V_2_8_2]] = None
    store_deploy_configs: Optional[List[Config_V_2_8_2]] = None
    if deploy_draft_configs:
        store_draft_configs = [
            Config_V_2_8_2(configuration=Configuration_V_2_8_2(
                commit_id=None,
                object_type=ConfigurationType_V_2_8_2(c.object_type), # Raises ValueErro() if invalid.
                path=c.path,
                recursive=c.recursive,
            ))
            for c in deploy_draft_configs
        ]
            
    if redeploy_deployed_configs:    
        store_deploy_configs = [
            Config_V_2_8_2(configuration=Configuration_V_2_8_2(
                commit_id=c.commit_id,
                object_type=ConfigurationType_V_2_8_2(c.object_type), # Raises ValueError() if invalid.
                path=c.path,
                recursive=c.recursive,
            ))
            for c in redeploy_deployed_configs
        ]
    
    res_store: Optional[DeployablesValidFilter_V_2_8_2] = None
    if (store_draft_configs or store_deploy_configs):
        res_store = DeployablesValidFilter_V_2_8_2(
            draft_configurations=store_draft_configs, 
            deploy_configurations=store_deploy_configs
        )
    
    # Result
    return DeployFilter_V_2_8_2(
        controller_ids=[controller_id],
        delete=res_delete,
        store=res_store,
        add_orders_date_from=None, # now()
        include_late=None,
        audit_log=res_audit_log,
    )