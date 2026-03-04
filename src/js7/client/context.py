from ..model.configuration.auth_configuration import AuthConfiguration
from ..model.configuration.http_configuration import HTTPConfiguration
from ..model.configuration.client_configuration import ClientConfiguration
from .auth.auth_provider import AuthProvider
from ..service.http_service import HTTPService
from ..api.joc.interface.interface import Interface as JOCInterface

from ..validator.http.joc_http_status_validator import joc_http_status_validator


class Context:
    def __init__(self, *, http_config: HTTPConfiguration, auth_config: AuthConfiguration, client_config: ClientConfiguration):
        # Initializes the joc api interface with auto discovery
        self.joc_api = JOCInterface(version=None)
        self.client_config = client_config
             
        self.http_service = HTTPService(
            configuration=http_config,
            response_validator=joc_http_status_validator
        )
        
        self.auth_provider = AuthProvider(
            http_service=self.http_service, 
            joc_version=None, 
        )
        
        # Initial login
        self.auth_provider.login(
            auth_config=auth_config, 
            force_server_login=True
        )
        
        # Gets the joc version
        from .action.joc.get_version_action import get_version_action
        joc_version = get_version_action(context=self)
        self.version = joc_version
        
        # Disables auto discovery with version parameter
        self.joc_api.set_version(self.version)
        
