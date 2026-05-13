from dataclasses import dataclass
from typing import Optional

from ...api.joc.http.v_2_6_5.authentication.login import login as api_login, EndpointCall, Options
from ...service.http_service import HTTPService


@dataclass
class LoginResponse:
    access_token: str
    session_timeout: Optional[int]


def login(*, http_service: HTTPService, basic_auth: Optional[str]) -> LoginResponse:
    result = api_login(EndpointCall(
        http_service=http_service,
        options=Options(
            basic_auth=basic_auth
        )
    ))
    
    if not result.access_token:
        raise ValueError("Authentication response does not contain an access token.")
    
    if all([result.access_token, result.session_timeout]):
        return LoginResponse(access_token=result.access_token, session_timeout=result.session_timeout)   

    raise RuntimeError("Response model is unknown.")

