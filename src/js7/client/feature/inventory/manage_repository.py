from typing import List, Literal, Optional, Union

from ...context import Context
from ....model.public.client.common.git_credentials import GitCredentials
from ....model.public.client.common.configurations import Configuration, DeployConfiguration, DraftConfiguration, ReleaseConfiguration
from ....model.public.client.common.audit_log import AuditLog

from ...action.inventory.get_git_credentials_action import get_git_credentials_action
from ...action.inventory.git_add_action import git_add_action
from ...action.inventory.git_checkout_action import git_checkout_action
from ...action.inventory.git_clone_action import git_clone_action
from ...action.inventory.git_commit_action import git_commit_action
from ...action.inventory.git_pull_action import git_pull_action
from ...action.inventory.git_push_action import git_push_action
from ...action.inventory.remove_git_credentials_action import remove_git_credentials_action
from ...action.inventory.store_git_credentials_action import store_git_credentials_action
from ...action.inventory.read_from_local_repository_action import read_from_local_repository_action
from ...action.inventory.remove_repository_configuration_action import remove_repository_configuration_action
from ...action.inventory.store_repository_configuration_action import store_repository_configuration_action
from ...action.inventory.update_repository_configuration_action import update_repository_configuration_action


class ManageRepository:
    """Manages Repository objects."""
    
    def __init__(self, context: Context):
        self._ctx = context

    def get_git_credentials(self) -> GitCredentials:
        """
        Retrieve the stored Git credentials for the current JOC account.

        Returns:
            GitCredentials:
                The stored Git credentials.

        Raises:
            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """

        return get_git_credentials_action(context=self._ctx)

    def git_add(
        self, 
        folder_path: str, 
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Add all unstaged changes (tracked and untracked) to the staging area
        of the specified local repository.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """

        return git_add_action(
            context=self._ctx, 
            folder_path=folder_path, 
            category=category, 
            audit_log=audit_log
        )

    def git_checkout(
        self,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        branch: Optional[str] = None,
        tag: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Check out a specific branch or tag in the specified local repository.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            branch (Optional[str]):
                The name of the branch to check out.

            tag (Optional[str]):
                The name of the tag to check out.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If both `branch` and `tag` are specified or arguments are invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return git_checkout_action(
            context=self._ctx,
            folder_path=folder_path,
            category=category,
            branch=branch,
            tag=tag,
            audit_log=audit_log
        )
        
    def git_clone(
        self,
        remote_url: str,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Clones a remote repository into a local repository folder.

        Args:
            remote_url (str):
                The URL of the remote repository.

            folder_path (str):
                The target path of the local repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If cloning fails or the server version is incompatible.
        """
        
        return git_clone_action(
            context=self._ctx,
            remote_url=remote_url,
            folder_path=folder_path,
            category=category,
            audit_log=audit_log
        )

    def git_commit(
        self,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        message: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Commit all staged changes in the specified local repository.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            message (Optional[str]):
                The commit message.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the commit fails or the server version is incompatible.
        """
        
        return git_commit_action(
            context=self._ctx,
            folder_path=folder_path,
            category=category,
            message=message,
            audit_log=audit_log
        )
        
    def git_pull(
        self,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Pull recent changes from the remote repository into the specified
        local repository.

        If merge conflicts occur, they must be resolved outside of JOC Cockpit.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.
                
            RuntimeError:
                If the pull operation fails or the server version is incompatible.
        """
        
        return git_pull_action(
            context=self._ctx,
            folder_path=folder_path,
            category=category,
            audit_log=audit_log
        )
        
    def git_push(
        self,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Push committed changes to the remote repository.

        If merge conflicts occur, they must be resolved outside of JOC Cockpit.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.
                
            RuntimeError:
                If the push operation fails or the server version is incompatible.
        """
        
        return git_push_action(
            context=self._ctx,
            folder_path=folder_path,
            category=category,
            audit_log=audit_log
        )
    
    def remove_git_credentials(self, git_server: str, audit_log: Optional[AuditLog] = None) -> bool:
        """
        Remove Git credentials for the current JOC account,
        depending on the configured JOC security levels.

        Args:
            git_server (str):
                The Git server for which the credentials should be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return remove_git_credentials_action(
            context=self._ctx,
            git_server=git_server,
            audit_log=audit_log
        )
        
    def store_git_credentials(
        self,
        credentials: GitCredentials,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store Git credentials for the current JOC account,
        depending on the configured JOC security levels.

        Args:
            credentials (GitCredentials):
                The Git credentials to be stored.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return store_git_credentials_action(
            context=self._ctx,
            credentials=credentials,
            audit_log=audit_log
        )

    def read_from_local_repository(
        self,
        folder_path: str,
        category: Literal['LOCAL', 'ROLLOUT']
    ) -> List[Configuration]:
        """
        Read configuration objects from a local repository located at
        `./resources/joc/repositories`.

        Args:
            folder_path (str):
                The path of the repository folder.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

        Returns:
            List[Configuration]:
                A list of configuration objects read from the repository.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If reading fails or the server version is incompatible.
        """
        
        return read_from_local_repository_action(
            context=self._ctx,
            folder_path=folder_path,
            category=category
        )
    
    def remove_repository_configuration(
        self,
        configurations: List[Configuration],
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Delete configuration objects from a local repository located at
        `./resources/joc/repositories`.

        If the object type `FOLDER` is specified, all configurations within
        that folder will be deleted from the local repository.

        Args:
            configurations (List[Configuration]):
                The configuration objects to be deleted.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return remove_repository_configuration_action(
            context=self._ctx,
            configurations=configurations,
            category=category,
            audit_log=audit_log
        )
    
    def store_repository_configuration(
        self,
        controller_id: str,
        category: Literal['LOCAL', 'ROLLOUT'],
        configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store configuration objects in a local repository located at
        `./resources/joc/repositories`.

        Args:
            controller_id (str):
                The ID of the controller associated with the configurations.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            configurations (List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]]):
                The configuration objects to be stored.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """

        return store_repository_configuration_action(
            context=self._ctx,
            controller_id=controller_id,
            category=category,
            configurations=configurations,
            audit_log=audit_log
        )
    
    def update_repository_configuration(
        self,
        configurations: List[Configuration],
        category: Literal['LOCAL', 'ROLLOUT'],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Add or update configuration objects in JOC using configurations
        from the local repository.

        Args:
            configurations (List[Configuration]):
                The configuration objects to be added or updated.

            category (Literal["LOCAL", "ROLLOUT"]):
                The repository category.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return update_repository_configuration_action(
            context=self._ctx,
            configurations=configurations,
            category=category,
            audit_log=audit_log
        )
