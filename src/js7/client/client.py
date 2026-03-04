from functools import cached_property
from pathlib import Path
from typing import Optional, Union

from .context import Context
from ..model.configuration.http_configuration import HTTPConfiguration
from ..model.configuration.client_configuration import ClientConfiguration
from ..model.configuration.auth_configuration import AuthConfiguration

from .feature.inventory.inventory import Inventory
from .feature.order.order import Order
from .feature.joc.joc import JOC
from .feature.agent.agent import Agent
from .feature.task.task import Task
from .feature.workflow.workflow import Workflow
from .feature.controller.controller import Controller
from .feature.iam.iam import IAM
from .feature.daily_plan.daily_plan import DailyPlan

from .action.helper.encrypt_action import encrypt_action
from .action.helper.decrypt_action import decrypt_action


class Client:
    """
    The `Client` class serves as the central entry point for interacting with JS7 JOC.

    Args:
        http_config (HTTPConfiguration):
            Configuration of the HTTP connection to the JOC endpoint

        auth_config (AuthConfiguration):
            Configuration for authentication. Supported methods include
            basic authentication and certificate-based authentication.

        client_config (ClientConfiguration):
            Configuration of the client’s behavior.

    Returns:
        Client:
            An instance of the `Client` class that can be used to perform operations against JS7 JOC.
    """
    
    def __init__(
        self, 
        *, 
        http_config: HTTPConfiguration, 
        auth_config: AuthConfiguration, 
        client_config: ClientConfiguration = ClientConfiguration()
    ):

        self._ctx = Context(
            http_config=http_config,
            auth_config=auth_config,
            client_config=client_config
        )
    
    @cached_property
    def inventory(self) -> Inventory:
        return Inventory(context=self._ctx)
    
    @cached_property
    def order(self) -> Order:
        return Order(context=self._ctx)
    
    @cached_property
    def joc(self) -> JOC:
        return JOC(context=self._ctx)
    
    @cached_property
    def agent(self) -> Agent:
        return Agent(context=self._ctx)
    
    @cached_property
    def task(self) -> Task:
        return Task(context=self._ctx)
    
    @cached_property
    def workflow(self) -> Workflow:
        return Workflow(context=self._ctx)
    
    @cached_property
    def controller(self) -> Controller:
        return Controller(context=self._ctx)
    
    @cached_property
    def iam(self) -> IAM:
        return IAM(context=self._ctx)
    
    @cached_property
    def daily_plan(self) -> DailyPlan:
        return DailyPlan(context=self._ctx)
        
    def login(self, auth_config: Optional[AuthConfiguration] = None, force_server_login: bool = False) -> str:
        """
        Args:
            auth_config (Optional[AuthConfiguration]):
                Configuration object for authentication. Supported methods are
                basic authentication and certificate-based authentication.

            force_server_login (bool):
                If set to ``True``, any existing stored session will be ignored
                and a new login will be performed. In this case, ``auth_config``
                must be provided.

        Returns:
            str:
                The access token as a string.
                
        Raises:
            ValueError:
                If the provided input data is invalid.

            RuntimeError:
                If neither certificate-based authentication nor basic authentication
                is available in exceptional cases.
        """
        
        return self._ctx.auth_provider.login(auth_config=auth_config, force_server_login=force_server_login)

    def logout(self) -> bool:
        """
        Logs the user out from the server and clears the local session.

        Returns:
            bool:
                `True` if the server-side logout was successful, otherwise `False`.
                The local session is always cleared, regardless of the server response.
        """
        
        return self._ctx.auth_provider.logout()
    
    def encrypt(
        self,
        java_bin_path: Union[Path, str],
        cert_file_path: Union[Path, str],
        in_string: Optional[str] = None,
        in_file: Optional[Union[Path, str]] = None,
        out_path: Optional[Union[Path, str]] = None,
    ) -> str:
        """
        Encrypts data using the JS7 Java encryption utility.

        This method wraps the JS7 `com.sos.commons.encryption.executable.Encrypt`
        class and executes it via a Java subprocess.

        Args:
            java_bin_path (Union[Path, str]):
                Path to the Java executable (e.g. `/usr/bin/java` on Linux).

            cert_file_path (Union[Path, str]):
                Path to the X.509 certificate file containing the public key
                used for encryption.

            in_string (Optional[str]):
                Plain text string to be encrypted.
                Either `in_string` or `in_file` must be provided, but not both.

            in_file (Optional[Union[Path, str]]):
                Path to the file to be encrypted.
                Either `in_string` or `in_file` must be provided, but not both.
                If `in_file` is used, `out_path` may optionally be provided to
                write the encrypted result to a file.

            out_path (Optional[Union[Path, str]]):
                Optional output file path where the encrypted result will be written.
                If omitted, the encrypted value is returned from stdout.

        Returns:
            str:
                The encrypted value as a string prefixed with `"enc:"`.

        Raises:
            ValueError:
                If input parameters are invalid (e.g. missing required arguments,
                non-existing paths, conflicting parameters).

            RuntimeError:
                If the underlying Java encryption process fails.
        """
        
        return encrypt_action(
            java_bin_path=java_bin_path,
            cert_file_path=cert_file_path,
            in_string=in_string,
            in_file=in_file,
            out_path=out_path
        )
        
    def decrypt(
        self,
        java_bin_path: Union[Path, str],
        key_file_path: Union[Path, str],
        key_password: Optional[str] = None,
        in_string: Optional[str] = None,
        in_file: Optional[Union[Path, str]] = None,
        out_path: Optional[Union[Path, str]] = None,
    ) -> str:
        """
        Decrypts data using the JS7 Java decryption utility.

        This method wraps the JS7 `com.sos.commons.encryption.executable.Decrypt`
        class and executes it via a Java subprocess.

        Args:
            java_bin_path (Union[Path, str]):
                Path to the Java executable (e.g. `/usr/bin/java` on Linux).

            key_file_path (Union[Path, str]):
                Path to the private key file used for decryption.

            key_password (Optional[str]):
                Optional password for the private key, if the key is encrypted.

            in_string (Optional[str]):
                Encrypted string to be decrypted. The value may optionally include
                the `"enc:"` prefix. Either `in_string` or `in_file` must be provided,
                but not both.

            in_file (Optional[Union[Path, str]]):
                Path to a file containing encrypted content.
                Either `in_string` or `in_file` must be provided, but not both.
                If `in_file` is used, `out_path` may optionally be provided to
                write the decrypted result to a file.

            out_path (Optional[Union[Path, str]]):
                Optional output file path where the decrypted result will be written.
                If omitted, the decrypted value is returned from stdout.

        Returns:
            str:
                The decrypted plain text.

        Raises:
            ValueError:
                If input parameters are invalid (e.g. missing required arguments,
                non-existing paths, conflicting parameters).

            RuntimeError:
                If the underlying Java decryption process fails.
        """
        
        return decrypt_action(
            java_bin_path=java_bin_path,
            key_file_path=key_file_path,
            key_password=key_password,
            in_string=in_string,
            in_file=in_file,
            out_path=out_path
        )
