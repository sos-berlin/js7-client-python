from typing import Any, Dict, List, Optional, Tuple

from ....client.context import Context

from ....model.public.client.common.audit_log import AuditLog

from ...action.joc.get_license_info_action import get_license_info_action
from ...action.joc.get_components_versions_action import get_components_versions_action
from ...action.joc.get_version_action import get_version_action
from ...action.joc.get_settings_action import get_settings_action
from ...action.joc.store_settings_action import store_settings_action


class Manage:    
    def __init__(self, context: Context):
        self._ctx = context
    
    def get_license_info(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Retrieve license validation status and related metadata.

        Returns:
            Tuple (bool, Dict[str, Any]):
                - bool: Indicates whether the license is valid
                (`True` if valid, otherwise `False`).
                - Dict[str, Any]: Additional information about the
                current license.

        Raises:
            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return get_license_info_action(context=self._ctx)
    
    def get_components_versions_info(
        self, 
        controller_ids: Optional[List[str]] = None, 
        agent_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve version information for specified JS7 components.

        Args:
            controller_ids (Optional[List[str]]):
                A list of controller IDs for which version information
                should be retrieved.

            agent_ids (Optional[List[str]]):
                A list of agent IDs for which version information
                should be retrieved.

        Returns:
            Dict[str, Any]:
                A dictionary containing version details for the
                requested components.

        Raises:
            ValueError:
                If arguments are invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_components_versions_action(
            context=self._ctx,
            controller_ids=controller_ids,
            agent_ids=agent_ids
        )
        
    def get_version(self) -> str:
        """
        Retrieve the JOC version with which the client
        is currently registered.

        Returns:
            str:
                The version string of the connected JOC instance.

        Raises:
            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_version_action(context=self._ctx)
    
    def get_settings_info(self) -> Dict[str, Any]:
        """
        Retrieve the global JOC settings.

        Returns:
            Dict[str, Any]:
                A dictionary containing the current global settings.

        Raises:
            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_settings_action(context=self._ctx)

    def store_settings(self, payload: Dict[str, Any], audit_log: Optional[AuditLog] = None) -> bool:
        """
        Store global JOC settings.

        Args:
            payload (Dict[str, Any]):
                A dictionary representing the settings to be stored.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns ``True`` if the settings were successfully stored,
                otherwise ``False``.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return store_settings_action(
            context=self._ctx,
            payload=payload,
            audit_log=audit_log
        )