from typing import List, Optional, Union

from ...context import Context
from ....model.public.client.common.identity_service import IdentityService
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    IdentityServiceFilter as IdentityServiceFilter_V_2_8_2,
    IdentityService as IdentityService_V_2_8_2,
    IdentityServices as IdentityServices_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_identity_services_action(
    *, 
    context: Context,
    identity_service_name: Optional[str]
) -> List[IdentityService]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        result = _build_v_2_8_2_request(
            context=context,
            identity_service_name=identity_service_name
        )
        
        services: List[IdentityService] = []
        
        if isinstance(result, IdentityServices_V_2_8_2):
            if result.identity_service_items:  
                for s in result.identity_service_items:
                    services.append(IdentityService(
                        identity_service_name=s.identity_service_name,
                        identity_service_type=s.identity_service_type.value if s.identity_service_type else "UNKNOWN",
                        service_authentication_scheme=s.service_authentication_scheme.value,
                        second_factor=s.second_factor or False,
                        second_factor_identity_service_name=s.second_factor_identity_service_name,
                        disabled=s.disabled or False,
                        required=s.required or False,
                        ordering=s.ordering or 1
                    ))
        else:
            services.append(IdentityService(
                identity_service_name=result.identity_service_name,
                identity_service_type=result.identity_service_type.value if result.identity_service_type else "UNKNOWN",
                service_authentication_scheme=result.service_authentication_scheme.value,
                second_factor=result.second_factor or False,
                second_factor_identity_service_name=result.second_factor_identity_service_name,
                disabled=result.disabled or False,
                required=result.required or False,
                ordering=result.ordering or 1
            ))
            
        return services
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    context: Context,
    identity_service_name: Optional[str]
) -> Union[IdentityServices_V_2_8_2, IdentityService_V_2_8_2]:
    
    if not identity_service_name:
        # Build: services_req
        services_req = IdentityServiceFilter_V_2_8_2(
            identity_service_name=None,
        )
        
        # Calls the dispatcher for the matching JOC version
        services_res = context.joc_api.dispatch(endpoint_id="iam/identityservices", call=EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=services_req,
            options=None,
        ))
        
        if not isinstance(services_res, IdentityServices_V_2_8_2):
            raise RuntimeError(f"Unexpected response type: {type(services_res).__name__}")
        
        return services_res
    
    # Build: service_req
    service_req = IdentityServiceFilter_V_2_8_2(
        identity_service_name=identity_service_name
    )
    
    # Calls the dispatcher for the matching JOC version
    service_res = context.joc_api.dispatch(endpoint_id="iam/identityservice", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=service_req,
        options=None,
    ))
    
    if not isinstance(service_res, IdentityService_V_2_8_2):
        raise RuntimeError(f"Unexpected response type: {type(service_res).__name__}")
    
    return service_res