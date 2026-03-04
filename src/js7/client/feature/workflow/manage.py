from typing import Dict

from ....client.context import Context

from ...action.workflow.get_workflow_versions_action import get_workflow_versions_action


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
        
    