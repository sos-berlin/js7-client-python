from ...model.private.api.endpoint import EndpointCall
from ...service.http_service import HTTPService
from ...model.private.http.joc.joc_v_2_8_2 import Authentication as Authentication_V_2_8_2
from ...api.joc.interface.interface import Interface


def logout(*, http_service: HTTPService, access_token: str) -> bool:
    joc_in = Interface(version=None)
    
    result = joc_in.dispatch(endpoint_id="authentication/logout", call=EndpointCall(
        http_service=http_service,
        access_token=access_token,
        options=None
    ))
        
    if isinstance(result, Authentication_V_2_8_2):
        if not result.is_authenticated:
            return True
        else:
            return False
    
    raise RuntimeError("Response model is unknown")