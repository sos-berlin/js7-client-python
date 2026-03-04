from dataclasses import dataclass
from typing import Optional


from ...api.joc.interface.interface import Interface
from ...service.http_service import HTTPService
from ...model.private.http.joc.joc_v_2_8_2 import Authentication as Authentication_V_2_8_2
from ...model.private.api.endpoint import EndpointCall


@dataclass
class LoginResponse:
    access_token: str
    session_timeout: Optional[int]


def login(*, http_service: HTTPService, basic_auth: Optional[str]) -> LoginResponse:
    joc_in = Interface(version=None)
    
    result = joc_in.dispatch(endpoint_id="authentication/login", call=EndpointCall(
        http_service=http_service,
        access_token=None,
        options={ "basic_auth": basic_auth }
    ))

    if isinstance(result, Authentication_V_2_8_2):
        if not result.access_token:
            raise ValueError("Authentication response does not contain an access token.")
        
        if all([result.access_token, result.session_timeout]):
            return LoginResponse(access_token=result.access_token, session_timeout=result.session_timeout)     
    
    raise RuntimeError("Response model is unknown")

