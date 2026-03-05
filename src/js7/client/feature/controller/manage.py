from typing import Any, Dict, Literal, Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.controller.test_controller_instance_action import test_controller_instance_action
from ...action.controller.confirm_cluster_node_loss_action import confirm_cluster_node_loss_action
from ...action.controller.get_controller_components_action import get_controller_components_action
from ...action.controller.get_controller_status_action import get_controller_status_action
from ...action.controller.register_controller_action import register_controller_action
from ...action.controller.unregister_controller_action import unregister_controller_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
        
    def test_controller_instance(
        self,
        url: str,
        controller_id: Optional[str] = None,
    ) -> bool:
        """
        Tests the connectivity of a Controller instance and optionally verifies its Controller ID.

        Args:
            url (str):
                The URL of the Controller instance against which the connection test is performed.

            controller_id (Optional[str]):
                If provided, verifies that the Controller instance is registered with
                the specified Controller ID.

        Returns:
            bool:
                Returns `True` if the connection status is `established`.
                Returns `False` if the status is `unstable`, `unreachable`, or `unknown`.

        Raises:
            ValueError:
                If required arguments such as `url` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return test_controller_instance_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url
        )
        
    def confirm_cluster_node_loss(
        self,
        controller_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Confirms that a Controller node in the cluster is permanently lost.

        Args:
            controller_id (str):
                The unique identifier of the Controller instance that is
                expected to be lost.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the specified Controller node is confirmed as lost,
                otherwise returns `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return confirm_cluster_node_loss_action(
            context=self._ctx,
            controller_id=controller_id,
            audit_log=audit_log
        )
        
    def get_controller_components(self, controller_id: str) -> Dict[str, Any]:
        """
        Retrieves the components of the specified Controller instance.

        Args:
            controller_id (str):
                The unique identifier of the Controller instance for which
                component information is requested.

        Returns:
            Dict ([str, Any]):
                A dictionary containing details about the Controller components.

        Raises:
            ValueError:
                If required arguments such as `controller_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_controller_components_action(
            context=self._ctx,
            controller_id=controller_id
        )
        
    def get_controller_status(
        self,
        controller_id: str,
        url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> Dict[str, Any]:
        """
        Gets Controller status information.
        
        Args:
            controller_id (str):
                The unique identifier of the Controller instance for which
                status information is requested.
                
            url (str):
                URL of the Controller instance. This parameter is required for a Controller cluster.
                
        Returns:
            Dict ([str, Any]):
                A dictionary containing details about the Controller status.
                
        Raises:
            ValueError:
                If required arguments such as `controller_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_controller_status_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url,
            audit_log=audit_log
        )
        
    def register_controller(
        self,
        url: str,
        role: Literal['STANDALONE', 'PRIMARY', 'BACKUP'],
        controller_id: Optional[str] = None,
        title: Optional[str] = None,
        cluster_url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Registers a Controller or Controller cluster in JOC Cockpit.

        A Controller can be either a standalone instance or part of a cluster
        with PRIMARY and BACKUP roles. This operation adds a new Controller
        (or cluster) to JOC Cockpit or updates existing Controller information
        such as the URL or title.

        Args:
            url (str):
                The URL of the Controller instance.

            role (Literal['STANDALONE', 'PRIMARY', 'BACKUP']):
                The role of the Controller within the cluster.

            controller_id (Optional[str]):
                The Controller ID. Can be omitted only when registering
                a new Controller (cluster).

            title (Optional[str]):
                A display name used in JOC Cockpit.

            cluster_url (Optional[str]):
                For clustered Controllers only: The URL used by cluster
                nodes to communicate with each other.

            audit_log (Optional[AuditLog]):
                Optional audit log information to be included with the request.

        Returns:
            bool:
                Returns `True` if the Controller was successfully registered
                or updated.

        Raises:
            ValueError:
                If required arguments such as `url` or `role` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return register_controller_action(
            context=self._ctx,
            url=url,
            role=role,
            controller_id=controller_id,
            title=title,
            cluster_url=cluster_url,
            audit_log=audit_log
        )
    
    def unregister_controller(
        self,
        controller_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Unregisters a Controller instance.
        
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
            
            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.
                
        Returns:
            bool: 
                Returns `True` if the operation was successful, otherwise `False`.
                
        Raises:
            ValueError:
                If required arguments such as `controller_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return unregister_controller_action(
            context=self._ctx,
            controller_id=controller_id,
            audit_log=audit_log
        )
