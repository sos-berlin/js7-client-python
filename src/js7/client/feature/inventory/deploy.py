from pathlib import Path
from typing import List, Literal, Optional, Union
from cryptography.hazmat.primitives import hashes

from ...context import Context

from ....model.public.client.common.configurations import DeployConfiguration, DraftConfiguration
from ....model.public.client.common.audit_log import AuditLog

from ...action.inventory.deploy_configurations_action import deploy_configurations_action
from ...action.inventory.import_deploy_configurations_action import import_deploy_configurations_action


class Deploy:
    def __init__(self, context: Context):
        self._ctx = context
        
    def configurations(
        self,
        controller_id: str,
        delete: Optional[List[DeployConfiguration]] = None,
        deploy: Optional[List[DraftConfiguration]] = None,
        redeploy: Optional[List[DeployConfiguration]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Creates a deployment for configurations stored in the inventory
        to the specified controller.
        
        Please note that the controller processes the deployment asynchronously.
        A return value of `True` only indicates that both JOC and the controller have successfully received the command.

        The deployment can:
        - Deploy draft configurations,
        - Redeploy already deployed configurations,
        - Remove deployed configurations from the controller.

        Args:
            controller_id (str):
                The ID of the controller to which the deployment
                should be applied.

            delete (Optional[List[DeployConfiguration]]):
                A list of deployed configurations to be removed
                from the controller.

            deploy (Optional[List[DraftConfiguration]]):
                A list of draft configurations to be deployed.

            redeploy (Optional[List[DeployConfiguration]]):
                A list of already deployed configurations to be redeployed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the deployment was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the deployment fails or the server version
                is incompatible.
        """
                
        return deploy_configurations_action(
            context=self._ctx,
            controller_id=controller_id,
            delete_deployed_configs=delete,
            deploy_draft_configs=deploy,
            redeploy_deployed_configs=redeploy,
            audit_log=audit_log
        )
        
    def import_deploy_configurations(
        self,
        controller_id: str,
        file_path: Union[Path, str],
        private_key_file: Union[Path, str],
        public_key_file: Optional[Union[Path, str]] = None,
        key_password: Optional[bytes] = None,
        hash_alg: hashes.HashAlgorithm = hashes.SHA512(),
        archive_format: Literal["ZIP", "TAR_GZ"] = "ZIP",
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Imports and deploys inventory configurations to a JS7 Controller.

        This operation uploads configuration objects ('.json') or archives
        ('.zip', '.tar.gz', '.tgz') to JOC and immediately deploys them
        to the specified Controller.

        Unlike `import_configurations`, this method performs a signed
        deployment and therefore requires:

        - Security Level HIGH enabled in JOC
        - A valid private key for signing
        - A matching public key configured in JOC

        Supported inputs:
        - A single '.json' configuration file
        - A directory containing '.json' files (processed recursively)
        - ZIP or TAR.GZ archives containing '.json' files
        (archives inside directories are processed recursively)

        All configuration files are signed locally. For each '.json'
        file, a corresponding '.json.sig' file is generated and included
        in the uploaded archive.

        Args:
            controller_id (str):
                The identifier of the Controller to which the configurations
                should be deployed.

            file_path (Union[Path, str]):
                The local path to a configuration file, archive, or directory
                containing configuration files.

            private_key_file (Union[Path, str]):
                Path to the private key (PEM format) used to sign
                configuration files before deployment.

            public_key_file (Optional[Union[Path, str]]):
                Optional public key (PEM format) used for local
                signature verification prior to upload.

            key_password (Optional[bytes]):
                Optional password for an encrypted private key.

            hash_alg (hashes.HashAlgorithm):
                Hash algorithm used for signing (e.g. SHA256, SHA512).
                Defaults to SHA512.

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format created by the client before upload.
                Defaults to "ZIP".

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this deployment.

        Returns:
            bool:
                Returns `True` if the deployment was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required parameters are missing or invalid.

            RuntimeError:
                If the server version is incompatible, the signing process fails,
                or an unexpected response is returned.
        """
        
        return import_deploy_configurations_action(
            context=self._ctx,
            controller_id=controller_id,
            file_path=file_path,
            archive_format=archive_format,
            private_key_file=private_key_file,
            public_key_file=public_key_file,
            key_password=key_password,
            hash_alg=hash_alg,
            audit_log=audit_log
        )