from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from cryptography.hazmat.primitives import hashes

from .manage_repository import ManageRepository

from ...context import Context
from ....model.public.client.filter.export_filter import ExportFilter
from ....model.public.client.enum.object_types import ObjectType, ReleaseObjectType
from ....model.public.client.enum.operation_type import OperationType
from ....model.public.client.common.changes import Change, ChangeDependencies
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.filter.export_folders_filter import ExportFoldersFilter
from ....model.public.client.common.configurations import Configuration, DeployConfiguration, DraftConfiguration, ReleaseConfiguration

from ...action.inventory.export_folders_action import export_folders_action
from ...action.inventory.deploy_configurations_action import deploy_configurations_action
from ...action.inventory.recall_released_configuration_action import recall_released_configurations_action
from ...action.inventory.recall_folder_action import recall_folder_action
from ...action.inventory.release_configuartions_action import release_configuartions_action
from ...action.inventory.remove_folder_action import remove_folder_action
from ...action.inventory.remove_folder_from_trash_action import remove_folder_from_trash_action
from ...action.inventory.remove_configurations_action import remove_configurations_action
from ...action.inventory.remove_configurations_from_trash_action import remove_configurations_from_trash_action
from ...action.inventory.restore_configuration_from_trash_action import restore_configuration_from_trash_action
from ...action.inventory.validate_configuration_action import validate_configuration_action
from ...action.inventory.revoke_configurations_action import revoke_configurations_action
from ...action.inventory.store_configuration_action import store_configuration_action
from ...action.inventory.get_changes_action import get_changes_action
from ...action.inventory.get_change_dependencies_action import get_change_dependencies_action
from ...action.inventory.export_configurations_action import export_configurations_action
from ...action.inventory.import_configurations_action import import_configurations_action
from ...action.inventory.import_deploy_configurations_action import import_deploy_configurations_action


class Manage:
    """Manages inventory objects."""
    
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def repository(self) -> ManageRepository:
        return ManageRepository(context=self._ctx)
    
    def deploy_configurations(
        self,
        controller_id: str,
        delete: Optional[List[DeployConfiguration]] = None,
        deploy: Optional[List[DraftConfiguration]] = None,
        redeploy: Optional[List[DeployConfiguration]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Create a deployment for configurations stored in the inventory
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
    
    def export_folders(
        self,
        controller_id: str,
        out_dir: Union[Path, str],
        filter: ExportFoldersFilter,
        filename: str = "export.zip",
        archive_format: Literal["ZIP", "TAR_GZ"] = "ZIP",
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Export inventory configurations as an archive file.

        Draft, deployed, and released configurations can be exported
        based on the provided filter criteria.

        Args:
            controller_id (str):
                The ID of the controller associated with the export.

            out_dir (Union[Path, str]):
                The target directory where the archive file will be created.

            filter (ExportFoldersFilter):
                Defines which folders and object types should be exported.

            filename (str):
                The name of the archive file. Defaults to "export.zip".

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format to be created. Defaults to "ZIP".

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the export was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the export fails or the server version
                is incompatible.
        """
        
        return export_folders_action(
            context=self._ctx,
            controller_id=controller_id,
            out_dir=out_dir,
            filename=filename,
            archive_format=archive_format,
            filter=filter,
            audit_log=audit_log
        )

    def recall_released_configurations(
        self,
        configurations: List[ReleaseConfiguration],
        audit_log: Optional[AuditLog]
    ) -> bool:
        """
        Recall previously released configurations.

        Args:
            configurations (List[ReleaseConfiguration]):
                The released configurations to be recalled.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the recall was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return recall_released_configurations_action(
            context=self._ctx,
            configurations=configurations,
            audit_log=audit_log
        )
        
    def recall_folder(
        self,
        folder_path: str,
        filter_object_types: Optional[List[ReleaseObjectType]] = None,
        filter_no_invalid_objects: bool = False,
        recursive: bool = True,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Recall released configurations from a folder.

        Args:
            folder_path (str):
                The path of the folder containing released configurations.

            filter_object_types (Optional[List[ReleaseObjectType]]):
                Restricts the recall operation to specific object types.

            filter_no_invalid_objects (bool):
                If `True`, excludes invalid objects from the recall.
                Defaults to `False`.

            recursive (bool):
                If `True`, includes subfolders recursively.
                Defaults to `True`.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the recall was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """

        return recall_folder_action(
            context=self._ctx,
            folder_path=folder_path,
            filter_object_types=filter_object_types,
            filter_no_invalid_objects=filter_no_invalid_objects,
            recursive=recursive,
            audit_log=audit_log
        )
    
    def release_configuartions(
        self,
        update: Optional[List[ReleaseConfiguration]] = None,
        delete: Optional[List[ReleaseConfiguration]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Release configurations by path and object type.

        Args:
            update (Optional[List[ReleaseConfiguration]]):
                Configurations to be released or updated.

            delete (Optional[List[ReleaseConfiguration]]):
                Released configurations to be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the release was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return release_configuartions_action(
            context=self._ctx,
            update=update,
            delete=delete,
            audit_log=audit_log
        )
    
    def remove_folder(
        self,
        folder_path: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Remove a folder containing inventory configurations.

        Args:
            folder_path (str):
                The path of the folder to be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the folder was successfully removed,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return remove_folder_action(
            context=self._ctx,
            folder_path=folder_path,
            audit_log=audit_log
        )
    
    def remove_folder_from_trash_action(
        self,
        folder_path: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Permanently delete a folder from the inventory trash.

        Args:
            folder_path (str):
                The path of the folder to be permanently deleted.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the folder was permanently deleted,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return remove_folder_from_trash_action(
            context=self._ctx,
            folder_path=folder_path,
            audit_log=audit_log
        )
        
    def remove_configuration(
        self,
        configurations: List[Configuration],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Remove inventory configurations.

        Args:
            configurations (List[Configuration]):
                The configurations to be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the configurations were successfully removed,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return remove_configurations_action(
            context=self._ctx,
            configurations=configurations,
            audit_log=audit_log
        )
        
    def remove_configurations_from_trash(
        self,
        configurations: List[Configuration],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Permanently delete configurations from the inventory trash.

        Args:
            configurations (List[Configuration]):
                The configurations to be permanently deleted.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the configurations were permanently deleted,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return remove_configurations_from_trash_action(
            context=self._ctx,
            configurations=configurations,
            audit_log=audit_log
        )
        
    def restore_configuration_from_trash(
        self,
        configuration: Configuration,
        new_path: str,
        add_prefix: Optional[str] = None,
        add_suffix: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> str:
        """
        Restore a configuration from the inventory trash.

        Args:
            configuration (Configuration):
                The configuration to be restored.

            new_path (str):
                The target path where the configuration should be restored.

            add_prefix (Optional[str]):
                A prefix to be added to the restored configuration name.

            add_suffix (Optional[str]):
                A suffix to be added to the restored configuration name.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            str:
                The path of the restored configuration.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return restore_configuration_from_trash_action(
            context=self._ctx,
            configuration=configuration,
            new_path=new_path,
            add_prefix=add_prefix,
            add_suffix=add_suffix,
            audit_log=audit_log
        )
        
    def validate_configuration(
        self,
        object_type: ObjectType,
        file: Union[Path, str, Dict[str, Any]]
    ) -> bool:
        """
        Validate a configuration provided as a file path
        or as a JSON dictionary.

        Args:
            object_type (ObjectType):
                The type of the configuration object.

            file (Union[Path, str, Dict[str, Any]]):
                The configuration provided either as a file path
                or as a JSON dictionary.

        Returns:
            bool:
                Returns `True` if the configuration is valid,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If validation fails or the server version
                is incompatible.
        """
        
        return validate_configuration_action(
            context=self._ctx,
            object_type=object_type,
            file=file
        )
        
    def revoke_configurations_action(
        self,
        controller_ids: List[str],
        configurations: List[DeployConfiguration],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Revoke deployed configurations from the specified controllers.

        Args:
            controller_ids (List[str]):
                The IDs of the controllers from which the configurations
                should be revoked.

            configurations (List[DeployConfiguration]):
                The deployed configurations to be revoked.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the configurations were successfully revoked,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return revoke_configurations_action(
            context=self._ctx,
            controller_ids=controller_ids,
            configurations=configurations,
            audit_log=audit_log
        )
        
    def store_configuration(
        self,
        configuration: Configuration,
        payload: Optional[Dict[str, Any]] = None,
        no_invalid: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store an inventory configuration.

        Args:
            configuration (Configuration):
                The configuration metadata.

            payload (Optional[Dict[str, Any]]):
                The JSON payload representing the configuration content. 
                Can be `None` if only a folder is to be created.

            no_invalid (bool):
                If `True`, prevents storing invalid configurations.
                Defaults to `False`.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the configuration was successfully stored,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return store_configuration_action(
            context=self._ctx,
            configuration=configuration,
            payload=payload,
            no_invalid=no_invalid,
            audit_log=audit_log
        )
        
    def get_changes(self, names: List[str]) -> List[Change]:
        """
        Retrieve one or more changes by name.

        Args:
            names (List[str]):
                The names of the changes to be retrieved.

        Returns:
            List[Change]:
                A list of matching change objects.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_changes_action(
            context=self._ctx,
            names=names
        )
        
    def get_change_dependencies(
        self,
        operation_type: OperationType,
        changes: List[Change],
        filter_paths: Optional[List[str]] = None,
        filter_no_references: bool = False,
        filter_no_referencing: bool = False
    ) -> List[ChangeDependencies]:
        """
        Resolve the direct dependencies for the given changes
        within the specified operation context.

        Args:
            operation_type (OperationType):
                The operation context (e.g. DEPLOY, EXPORT)
                that defines how dependencies are evaluated.

            changes (List[Change]):
                The changes for which dependencies should be resolved.

            filter_paths (Optional[List[str]]):
                If provided, only dependencies whose path starts
                with one of these values will be included.

            filter_no_references (bool):
                If `True`, excludes outgoing references
                (objects referenced by the given changes).
                Defaults to `False`.

            filter_no_referencing (bool):
                If `True`, excludes incoming references
                (objects that reference the given changes).
                Defaults to `False`.

        Returns:
            List[ChangeDependencies]:
                A list of dependency results, each representing
                one root change and its direct dependencies.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If dependency resolution fails or the server version
                is incompatible.
        """
        
        return get_change_dependencies_action(
            context=self._ctx,
            operation_type=operation_type,
            changes=changes,
            filter_paths=filter_paths,
            filter_no_references=filter_no_references,
            filter_no_referencing=filter_no_referencing
        )
        
    def export_configurations(
        self,
        controller_id: str,
        out_dir: Union[Path, str],
        filter: ExportFilter,
        filename: str = "export.zip",
        archive_format: Literal["ZIP", "TAR_GZ"] = "ZIP",
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Export unsigned configuration files as an archive.

        The export creates an archive file (ZIP or TAR_GZ)
        containing unsigned JSON configuration files based
        on the specified filter criteria.

        Args:
            controller_id (str):
                The ID of the controller associated with the export.

            out_dir (Union[Path, str]):
                The target directory where the archive file
                will be created.

            filter (ExportFilter):
                Defines the criteria used to select the
                configurations to be exported.

            filename (str):
                The name of the archive file.
                Defaults to "export.zip".

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format to be created.
                Defaults to "ZIP".

            audit_log (Optional[AuditLog]):
                Optional audit log information to create
                an audit entry for this operation.

        Returns:
            bool:
                Returns `True` if the export was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the export fails or the server version
                is incompatible.
        """
        
        return export_configurations_action(
            context=self._ctx,
            controller_id=controller_id,
            out_dir=out_dir,
            filename=filename,
            filter=filter,
            archive_format=archive_format,
            audit_log=audit_log
        )
        
    def import_configurations(
        self,
        file_path: Union[Path, str],
        archive_format: Literal["ZIP", "TAR_GZ"] = "ZIP",
        overwrite: bool = False,
        inventory_target_folder: Optional[str] = None,
        add_suffix: Optional[str] = None,
        add_prefix: Optional[str] = None,
        overwrite_tags: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Import inventory configurations into JS7 JOC.

        Supported inputs:
        - ZIP or TAR.GZ archives ('.zip', '.tar.gz', '.tgz').
        If a directory contains multiple archives, all archives
        are processed recursively.
        - Directories containing '.json' configuration files
        (processed recursively).
        - A single '.json' configuration file.

        The import behavior can be customized using overwrite options,
        target folder settings, prefix/suffix handling, tag overwriting,
        and optional audit logging.

        Args:
            file_path (Union[Path, str]):
                The local path to the file or directory to be imported.

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format to be created by the client.
                This does not refer to the local format specified
                by `file_path`. Defaults to "ZIP".

            overwrite (bool):
                If `True`, existing inventory objects will be overwritten.
                Defaults to `False`.

            inventory_target_folder (Optional[str]):
                Specifies the target folder in the inventory where
                imported objects should be stored.

            add_suffix (Optional[str]):
                A suffix to be added to the names of imported objects.

            add_prefix (Optional[str]):
                A prefix to be added to the names of imported objects.

            overwrite_tags (bool):
                If `True`, existing tags of inventory objects will be
                overwritten. Defaults to `False`.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return import_configurations_action(
            context=self._ctx,
            file_path=file_path,
            archive_format=archive_format,
            overwrite=overwrite,
            target_folder=inventory_target_folder,
            suffix=add_suffix,
            prefix=add_prefix,
            overwrite_tags=overwrite_tags,
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
        Import and deploy inventory configurations to a JS7 Controller.

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
        
    