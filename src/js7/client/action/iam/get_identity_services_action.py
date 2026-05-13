from typing import List, Optional, Union

from ...context import Context
from ....model.public.client.common.identity_service import IdentityService
from ....api.joc.http.v_2_6_5.iam.identity_service.identity_service import identity_service, EndpointCall as IdentityServiceEndpointCall
from ....api.joc.http.v_2_6_5.iam.identity_services.identity_services import identity_services, EndpointCall as IdentityServicesEndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    IdentityServiceFilter as IdentityServiceFilter_V_2_6_5,
    IdentityService as IdentityService_V_2_6_5,
    IdentityServices as IdentityServices_V_2_6_5
)


def get_identity_services_action(
    *, 
    context: Context,
    identity_service_name: Optional[str]
) -> List[IdentityService]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = _build_v_2_6_5_request(
            context=context,
            identity_service_name=identity_service_name
        )
        
        services: List[IdentityService] = []
        
        if isinstance(result, IdentityServices_V_2_6_5):
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
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    context: Context,
    identity_service_name: Optional[str]
) -> Union[IdentityServices_V_2_6_5, IdentityService_V_2_6_5]:
    
    if not identity_service_name:
        # Build: services_req
        services_req = IdentityServiceFilter_V_2_6_5(
            identity_service_name=None,
        )
        
        services_res = identity_services(IdentityServicesEndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=services_req
        ))
        
        return services_res
    
    # Build: service_req
    service_req = IdentityServiceFilter_V_2_6_5(
        identity_service_name=identity_service_name
    )
    
    service_res = identity_service(IdentityServiceEndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=service_req,
    ))
    
    return service_res