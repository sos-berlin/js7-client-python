import base64, time
from typing import Optional

from ...service.http_service import HTTPService
from ...model.configuration.auth_configuration import AuthConfiguration

from .login import login as login_handler
from .logout import logout as logout_handler


class AuthProvider:
    def __init__(self, http_service: HTTPService, joc_version: Optional[str]):
        self._http_service = http_service
        self._joc_version = joc_version
        
        self._auth_cache: Optional[AuthConfiguration] = None
        self._access_token: Optional[str] = None
        self._access_token_expires_at: float = 0.0

    def _basic_auth_header(self, username: str, password: str) -> str:
        if not username or not password:
            raise ValueError("'username' or 'password' must not be empty.")
        
        token = f"{username}:{password}"
        encoded_token = base64.b64encode(token.encode("utf-8")).decode("ascii")
        return f"Basic {encoded_token}"
    
    def login(self, auth_config: Optional[AuthConfiguration] = None, force_server_login: bool = False) -> str:
        """Returns the access token"""

        # Returns the cached access token if it is still valid and no server login is forced
        if (
            self._access_token
            and self._access_token_expires_at > time.time()
            and not force_server_login
        ):
            return self._access_token

        if not auth_config:
            auth_config = self._auth_cache

        if not auth_config:
            raise ValueError(
                "Authentication failed. No credentials available for (re-)login."
            )

        # Performs certificate login
        if auth_config.cert_auth:
            # Sets cert file paths in server handler
            self._http_service.auth_certfile_path = auth_config.cert_auth.certfile_path
            self._http_service.auth_keyfile_path = auth_config.cert_auth.keyfile_path

            login_response = login_handler(
                http_service=self._http_service,
                basic_auth=None
            )

            self._auth_cache = auth_config
            self._access_token = login_response.access_token
            self._set_token_expiry(login_response.session_timeout)

            return self._access_token
        # Performs username & password login
        elif auth_config.basic_auth:
            if not auth_config.basic_auth.username or not auth_config.basic_auth.password:
                raise ValueError("'username' and 'password' are required.")

            basic_auth_str = self._basic_auth_header(
                auth_config.basic_auth.username,
                auth_config.basic_auth.password
            )

            login_response = login_handler(
                http_service=self._http_service,
                basic_auth=basic_auth_str
            )

            self._auth_cache = auth_config
            self._access_token = login_response.access_token
            self._set_token_expiry(login_response.session_timeout)

            return self._access_token
        else:
            raise RuntimeError(
                "Authentication failed. Neither certificate nor Basic Auth parameters are available."
            )

    def _set_token_expiry(self, session_timeout: Optional[float]) -> None:
        """Calculates the local token expiry from the server-provided session timeout."""
        
        if session_timeout:
            self._access_token_expires_at = time.time() + session_timeout / 1000
        else:
            # no timeout provided means the session does not expire
            self._access_token_expires_at = float("inf")
            
    def logout(self) -> bool:
        try:
            access_token = self.login()
            
            if not access_token:
                return False
            
            return logout_handler(
                http_service=self._http_service,
                access_token=access_token,
            )
        except Exception:
            return False
        finally:
            # Always clean up local state
            self._http_service.close()
            self._joc_version = None
            self._auth_cache = None
            self._access_token = None
            self._access_token_expires_at = 0.0
