from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple

from ....client.context import Context
from ....model.public.client.common.identity_service import IdentityService
from ....model.public.client.filter.element.folder import Folder
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.accounts import Account, BlockedAccount

from ...action.iam.get_accounts_action import get_accounts_action
from ...action.iam.store_account_action import store_account_action
from ...action.iam.get_blocked_accounts_action import get_blocked_accounts_action
from ...action.iam.rename_account_action import rename_account_action
from ...action.iam.remove_accounts_action import remove_accounts_action
from ...action.iam.get_account_permissions_action import get_account_permissions_action
from ...action.iam.change_account_password_action import change_account_password_action
from ...action.iam.reset_account_passwords_action import reset_account_passwords_action
from ...action.iam.enable_accounts_action import enable_accounts_action
from ...action.iam.disable_accounts_action import disable_accounts_action
from ...action.iam.block_account_action import block_account_action
from ...action.iam.unblock_accounts_action import unblock_accounts_action
from ...action.iam.get_roles_action import get_roles_action
from ...action.iam.store_role_action import store_role_action
from ...action.iam.rename_role_action import rename_role_action
from ...action.iam.remove_roles_action import remove_roles_action
from ...action.iam.get_permissions_action import get_permissions_action
from ...action.iam.set_permissions_action import set_permissions_action
from ...action.iam.rename_permission_action import rename_permission_action
from ...action.iam.remove_permissions_action import remove_permissions_action
from ...action.iam.get_folder_permissions_action import get_folder_permissions_action
from ...action.iam.set_folder_permissions_action import set_folder_permissions_action
from ...action.iam.rename_folder_permissions_action import rename_folder_permissions_action
from ...action.iam.remove_folder_permissions_action import remove_folder_permissions_action
from ...action.iam.get_identity_services_action import get_identity_services_action
from ...action.iam.store_identity_service_action import store_identity_service_action
from ...action.iam.rename_identity_service_action import rename_identity_service_action
from ...action.iam.remove_identity_service_action import remove_identity_service_action
from ...action.iam.get_identity_service_settings_action import get_identity_service_settings_action
from ...action.iam.store_identity_service_settings_action import store_identity_service_settings_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context

    def get_accounts(
        self,
        identity_service_name: str,
        filter_account_name: Optional[str] = None,
        filter_enabled: bool = False,
        filter_disabled: bool = False
    ) -> List[Account]:
        """
        Returns a collection of Accounts.
        
        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.
                
            filter_account_name (str):
                Retrieve the account with this name.
                
            filter_enabled (bool):
                If `True` retrieve only enabled accounts.
                
            filter_disabled (bool):
                If `True` retrieve only disabled accounts.
                
        Returns:
            List[Account]: Returns a collection of Accounts.
            
        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_accounts_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            filter_account_name=filter_account_name,
            filter_enabled=filter_enabled,
            filter_disabled=filter_disabled
        )
    
    def get_blocked_accounts(
        self,
        filter_date_from: Optional[datetime] = None,
        filter_date_to: Optional[datetime] = None,
        filter_account_name: Optional[str] = None
    ) -> List[BlockedAccount]:
        """
        Returns a collection of blocked accounts.

        Args:
            filter_date_from (Optional[datetime]):
                Filters blocked accounts starting from the specified date.

            filter_date_to (Optional[datetime]):
                Filters blocked accounts up to the specified date.

            filter_account_name (Optional[str]):
                If provided, filters the results by the specified account name.

        Returns:
            List[BlockedAccount]:
                A list of blocked accounts matching the given filter criteria.

        Raises:
            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_blocked_accounts_action(
            context=self._ctx,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            filter_account_name=filter_account_name
        )
    
    def store_account(
        self,
        account: Account,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stores an account in the Identity Service.

        Args:
            account (Account):
                The account to be created or stored in the Identity Service.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return store_account_action(
            context=self._ctx,
            account=account,
            audit_log=audit_log
        )
        
    def rename_account(
        self,
        identity_service_name: str,
        account_name: str,
        new_account_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Renames an account.
        
        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.
                
            account_name (str):
                The old name of the accoun.
                
            new_account_name (str):
                The new name of the account.
                
            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.
                
        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return rename_account_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_name=account_name,
            new_account_name=new_account_name,
            audit_log=audit_log
        )
        
    def remove_accounts(
        self,
        identity_service_name: str,
        account_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deletes accounts from an Identity Service.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_names (List[str]):
                A list of account names to be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return remove_accounts_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_names=account_names,
            audit_log=audit_log
        )
    
    def get_account_permissions(
        self,
        identity_service_name: str,
        account_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> Dict[str, Any]:
        """
        Returns the permissions for the specified account as they would apply
        when logging in with that account.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_name (str):
                The name of the account for which permissions are requested.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            Dict ([str, Any]):
                A dictionary containing the JSON representation of the
                permissions for the specified account.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_account_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_name=account_name,
            audit_log=audit_log
        )
        
    def change_account_password(
        self,
        identity_service_name: str,
        account_name: str,
        account_password: str,
        new_account_password: str,
        force_password_change: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Changes the password for the specified account.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_name (str):
                The name of the account whose password is to be changed.

            account_password (str):
                The current password of the account.

            new_account_password (str):
                The new password to be set for the account.

            force_password_change (bool):
                If `True`, the account will be required to change the password
                upon the next login.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return change_account_password_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_name=account_name,
            account_password=account_password,
            new_account_password=new_account_password,
            force_password_change=force_password_change,
            audit_log=audit_log
        )
        
    def reset_account_passwords(
        self,
        identity_service_name: str,
        account_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Resets the specified account to its initial password.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_name (str):
                The name of the account whose password is to be reset
                to the initial value.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return reset_account_passwords_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_names=account_names,
            audit_log=audit_log
        )
    
    def enable_accounts(
        self,
        identity_service_name: str,
        account_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Enables the specified accounts.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_names (List[str]):
                A list of account names to be enabled.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return enable_accounts_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_names=account_names,
            audit_log=audit_log
        )
        
    def disable_accounts(
        self,
        identity_service_name: str,
        account_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Disables the specified accounts.
        
        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            account_names (List[str]):
                A list of account names to be disabled.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return disable_accounts_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            account_names=account_names,
            audit_log=audit_log
        )
        
    def block_account(
        self,
        account_name: str,
        comment: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Blocks the specified account.

        Args:
            account_name (str):
                The name of the account to be blocked.

            comment (str):
                A comment to be associated with the blocked account,
                typically describing the reason for the action.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return block_account_action(
            context=self._ctx,
            account_name=account_name,
            comment=comment,
            audit_log=audit_log
        )
        
    def unblock_accounts(
        self,
        account_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Unblocks the specified accounts.

        Args:
            account_names (List[str]):
                A list of account names to be removed from the list
                of blocked accounts.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return unblock_accounts_action(
            context=self._ctx,
            account_names=account_names,
            audit_log=audit_log
        )
        
    def get_roles(self, identity_service_name: str) -> List[str]:
        """
        Returns a collection of roles for the specified Identity Service.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

        Returns:
            List[str]:
                A list of roles defined for the specified Identity Service.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_roles_action(
            context=self._ctx,
            identity_service_name=identity_service_name
        )
        
    def store_role(
        self,
        identity_service_name: str,
        role_name: str,
        ordering: Optional[int] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stores a new role in the Identity Service.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role to be stored.

            ordering (Optional[int]):
                The ordering value of the role, used to define its position
                relative to other roles.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return store_role_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            ordering=ordering,
            audit_log=audit_log
        )
        
    def rename_role(
        self,
        identity_service_name: str,
        role_name: str,
        new_role_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Benennt eine vorhandene Rolle um.
        
        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                Der Name der alten Rolle.

            new_role_name (str):
                Der neue Name der Rolle.
        
            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.
                
        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return rename_role_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            new_role_name=new_role_name,
            audit_log=audit_log
        )
        
    def remove_roles(
        self,
        identity_service_name: str,
        role_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deletes roles from the specified Identity Service.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_names (List[str]):
                A list of role names to be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return remove_roles_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_names=role_names,
            audit_log=audit_log
        )
        
    def get_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        permission_path: Optional[str] = None,
        controller_id: Optional[str] = None,
        without_excluded: bool = False
    ) -> List[Tuple[str, bool]]:
        """
        Returns one or more permissions for a given role and optional Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role for which permissions are requested.

            permission_path (Optional[str]):
                The specific permission path to be returned. If omitted,
                all permissions assigned to the role are returned.

            controller_id (Optional[str]):
                The Controller ID for which permissions are requested.
                If omitted, permissions are returned without filtering
                by Controller.

            without_excluded (bool):
                If `True`, permissions marked as excluded are skipped.

        Returns:
            List[Tuple[str, bool]]:
                A list of tuples in the format `(permission_path, excluded)`,
                where `permission_path` is the permission identifier and the
                boolean value indicates whether the permission is marked as excluded.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            permission_path=permission_path,
            controller_id=controller_id,
            without_excluded=without_excluded
        )
        
    def set_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        controller_id: str,
        permissions: List[Tuple[str, bool]],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stores permissions for a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role to which the permissions are assigned.

            controller_id (str):
                The Controller ID for which the permissions should be stored

            permissions (List[Tuple[str, bool]]):
                A list of tuples in the format `(permission_path, excluded)`,
                where `permission_path` is the permission identifier and the
                boolean value indicates whether the permission is marked as excluded.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return set_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id,
            permissions=permissions,
            audit_log=audit_log
        )
        
    def rename_permission(
        self,
        identity_service_name: str,
        permission_path: str,
        new_permission: Tuple[str, bool],
        role_name: str,
        controller_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Renames a permission for a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            permission_path (str):
                The current permission path to be renamed.

            new_permission (Tuple[str, bool]):
                A tuple in the format `(new_permission_path, excluded)`,
                where `new_permission_path` is the updated permission identifier
                and the boolean value indicates whether the permission is marked
                as excluded.

            role_name (str):
                The name of the role to which the permission is assigned.

            controller_id (str):
                The Controller ID for which the permission applies.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return rename_permission_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            permission_path=permission_path,
            new_permission=new_permission,
            role_name=role_name,
            controller_id=controller_id,
            audit_log=audit_log
        )
        
    def remove_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        permission_paths: List[str],
        controller_id: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deletes permissions from a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role from which the permissions are removed.

            permission_paths (List[str]):
                A list of permission paths to be deleted from the specified
                role and Controller ID.

            controller_id (str):
                The Controller ID for which the changes apply.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return remove_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            permission_paths=permission_paths,
            controller_id=controller_id,
            audit_log=audit_log
        )
        
    def get_folder_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        controller_id: str,
        folder_name: Optional[str] = None
    ) -> List[Folder]:
        """
        Returns a collection of folders for the given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role for which folders are requested.

            controller_id (str):
                The Controller ID for which folders should be returned.

            folder_name (Optional[str]):
                If provided, only the specified folder is returned.

        Returns:
            List[Folder]:
                A collection of folders associated with the specified
                role and Controller ID.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_folder_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id,
            folder_name=folder_name
        )
        
    def set_folder_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        controller_id: str,
        folders: List[Folder],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stores folders for a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role for which the folders should be stored.

            controller_id (str):
                The Controller ID for which the folders should be stored

            folders (List[Folder]):
                A list of folders to be stored for the specified
                role and Controller ID.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return set_folder_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id,
            folders=folders,
            audit_log=audit_log
        )
        
    def rename_folder_permissions(
        self,
        identity_service_name: str,
        folder_name: str,
        new_folder: Folder,
        controller_id: str,
        role_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Renames a folder for a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            folder_name (str):
                The current name or path of the folder to be renamed.

            new_folder (Folder):
                The new folder definition, including the updated path
                and recursive settings.

            controller_id (str):
                The Controller ID for which the folder should be renamed.

            role_name (str):
                The name of the role for which the folder is assigned.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return rename_folder_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            folder_name=folder_name,
            new_folder=new_folder,
            controller_id=controller_id,
            role_name=role_name,
            audit_log=audit_log
        )
        
    def remove_folder_permissions(
        self,
        identity_service_name: str,
        role_name: str,
        controller_id: str,
        folder_names: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deletes folders from a given role and Controller ID.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be used for this operation.

            role_name (str):
                The name of the role from which the folders are removed.

            controller_id (str):
                The Controller ID for which the folders should be removed.

            folder_names (List[str]):
                A list of folder names to be deleted from the specified
                role and Controller ID.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return remove_folder_permissions_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            role_name=role_name,
            controller_id=controller_id,
            folder_names=folder_names,
            audit_log=audit_log
        )
        
    def get_identity_services(
        self, 
        identity_service_name: Optional[str] = None
    ) -> List[IdentityService]:
        """
        Returns a collection of Identity Services.

        Args:
            identity_service_name (Optional[str]):
                The name of the Identity Service. If `None`, all
                available Identity Services are returned.

        Returns:
            List[IdentityService]:
                A list of Identity Services matching the specified criteria.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_identity_services_action(
            context=self._ctx,
            identity_service_name=identity_service_name
        )
        
    def store_identity_service(
        self,
        identity_service: IdentityService,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stores an Identity Service.

        Args:
            identity_service (IdentityService):
                The Identity Service to be created stored.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return store_identity_service_action(
            context=self._ctx,
            identity_service=identity_service,
            audit_log=audit_log
        )
        
    def rename_identity_service(
        self,
        identity_service_name: str,
        new_identity_service_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Renames an Identity Service.

        Args:
            identity_service_name (str):
                The current name of the Identity Service to be renamed.

            new_identity_service_name (str):
                The new name to be assigned to the Identity Service.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return rename_identity_service_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            new_identity_service_name=new_identity_service_name,
            audit_log=audit_log
        )
        
    def remove_identity_service(
        self,
        identity_service_name: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deletes an Identity Service.

        Args:
            identity_service_name (str):
                The name of the Identity Service to be deleted.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return remove_identity_service_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            audit_log=audit_log
        )
        
    def get_identity_service_settings(
        self,
        identity_service_name: str,
        identity_service_type: Literal['KEYCLOAK', 'KEYCLOAK-JOC', 'LDAP', 'LDAP-JOC', 'OIDC', 'OIDC-JOC', 'FIDO', 'JOC', 'CERTIFICATE']
    ) -> Dict[str, Any]:
        """
        Retrieves the configuration settings of the specified Identity Service
        from the server database.

        Args:
            identity_service_name (str):
                The name of the Identity Service for which the configuration
                settings are requested.

            identity_service_type (Literal['KEYCLOAK', 'KEYCLOAK-JOC', 'LDAP', 'LDAP-JOC', 'OIDC', 'OIDC-JOC', 'FIDO', 'JOC', 'CERTIFICATE']):
                The type of the Identity Service whose configuration should be returned.

        Returns:
            Dict ([str, Any]):
                A dictionary containing the configuration settings of
                the specified Identity Service.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_identity_service_settings_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            identity_service_type=identity_service_type
        )
        
    def store_identity_service_settings(
        self,
        identity_service_name: str,
        identity_service_type: Literal['KEYCLOAK', 'KEYCLOAK-JOC', 'LDAP', 'LDAP-JOC', 'OIDC', 'OIDC-JOC', 'FIDO', 'JOC', 'CERTIFICATE'],
        settings: Dict[str, Any]
    ) -> bool:
        """
        Stores configuration settings for the specified Identity Service
        in the server database.

        Args:
            identity_service_name (str):
                The name of the Identity Service for which the configuration
                settings should be stored.

            identity_service_type (Literal['KEYCLOAK', 'KEYCLOAK-JOC', 'LDAP', 'LDAP-JOC', 'OIDC', 'OIDC-JOC', 'FIDO', 'JOC', 'CERTIFICATE']):
                The type of the Identity Service whose configuration is being stored.

            settings (Dict[str, Any]):
                A dictionary containing the configuration settings
                to be stored.

        Returns:
            bool:
                Returns `True` if the configuration was successfully stored.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return store_identity_service_settings_action(
            context=self._ctx,
            identity_service_name=identity_service_name,
            identity_service_type=identity_service_type,
            settings=settings
        )