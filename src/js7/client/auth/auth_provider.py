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
        
        # Checks whether the access token is still valid
        if self._access_token and self._access_token_expires_at > time.time():
            # Returns the cached access token if no forced server login is required
            if not force_server_login:
                return self._access_token
            
            # Return stored access token if no auth was provided
            if self._access_token and not auth_config:
                return self._access_token
            
        if not auth_config:
            self._auth_cache = None
            raise ValueError("Authentication failed.")
        
        # Performs certificate login
        if auth_config.cert_auth:
            # Sets cert file paths in server handler
            self._http_service.auth_certfile_path = auth_config.cert_auth.certfile_path
            self._http_service.auth_keyfile_path  = auth_config.cert_auth.keyfile_path
            
            login_response = login_handler(
                http_service=self._http_service,
                basic_auth=None
            )
            
            self._auth_cache = auth_config
            self._access_token = login_response.access_token
            
            if login_response.session_timeout:
                self._access_token_expires_at = time.time() + login_response.session_timeout / 1000
            else:
                self._access_token_expires_at = 0
            
            return self._access_token
        
        elif auth_config.basic_auth: # Performs username & password login
            if not auth_config.basic_auth.username or not auth_config.basic_auth.password:
                raise ValueError("'username' and 'password' are required.")
            
            basic_auth_str = self._basic_auth_header(auth_config.basic_auth.username, auth_config.basic_auth.password)
            
            login_response = login_handler(
                http_service=self._http_service,
                basic_auth=basic_auth_str
            )
            
            self._access_token = login_response.access_token
            
            if login_response.session_timeout:
                self._access_token_expires_at = time.time() + login_response.session_timeout / 1000
            else:
                self._access_token_expires_at = 0
            
            return self._access_token
        
        else:
            raise RuntimeError("Authentication failed. Neither certificate nor Basic Auth parameters are available.")
            
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
