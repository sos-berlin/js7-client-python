from ...service.http_service import HTTPService
from ...api.joc.http.v_2_6_5.authentication.logout import logout as api_logout, EndpointCall


def logout(*, http_service: HTTPService, access_token: str) -> bool:
    result = api_logout(EndpointCall(
        http_service=http_service,
        access_token=access_token,
    ))
        
    if not result.is_authenticated:
        return True
    else:
        return False

    raise RuntimeError("Response model is unknown.")