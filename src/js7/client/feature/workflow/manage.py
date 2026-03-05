from typing import Dict, Optional

from ....client.context import Context

from ....model.public.client.common.audit_log import AuditLog

from ...action.workflow.get_workflow_versions_action import get_workflow_versions_action
from ...action.workflow.set_workflow_version_as_current_action import set_workflow_version_as_current_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
        
    def get_workflow_versions(
        self,
        controller_id: str,
        workflow_path: str,
        exclude_current_version: bool = False
    ) -> Dict[str, str]:
        """
        Returns all versions of a given workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow whose versions should be retrieved.

            exclude_current_version (bool):
                If set to `True`, the currently active (current) version
                of the workflow will be excluded from the result.

        Returns:
            Dict ([str, str]):
                A dictionary mapping version id to workflow path
                in the format: `{version_id: workflow_path}`.

        Raises:
            ValueError:
                If required arguments such as `controller_id` or
                `workflow_path` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_workflow_versions_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            exclude_current_version=exclude_current_version
        )
        
    def set_workflow_version_as_current(
        self,
        controller_id: str,
        workflow_path: str,
        workflow_version_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Sets a specific workflow version as the current version for all orders.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow whose version should be updated.

            workflow_version_id (str):
                The workflow `version_id` that should be set as the current version.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful, otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`,
                `workflow_path`, or `workflow_version_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return set_workflow_version_as_current_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            workflow_version_id=workflow_version_id,
            audit_log=audit_log
        )
        
    