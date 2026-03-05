from typing import Optional
from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.controller.cancel_controller_action import cancel_controller_action
from ...action.controller.appoint_nodes_controller_action import appoint_controller_cluster_roles_action
from ...action.controller.cancel_and_restart_controller_action import cancel_and_restart_controller_action
from ...action.controller.switchover_controller_cluster_action import switchover_controller_cluster_action
from ...action.controller.restart_controller_action import restart_controller_action
from ...action.controller.terminate_controller_action import terminate_controller_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
        
    def appoint_controller_cluster_roles(
        self,
        controller_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Re-establishes Controller Cluster roles.
        
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
        
        return appoint_controller_cluster_roles_action(
            context=self._ctx,
            controller_id=controller_id,
            audit_log=audit_log
        )
        
    def cancel_and_restart_controller(
        self,
        controller_id: str,
        url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Aborts and restarts Controller and optionally switches over.
        
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
                
            url (str):
                URL of the Controller instance. This parameter is required for a Controller cluster.
                
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
        
        return cancel_and_restart_controller_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url,
            audit_log=audit_log
        )
        
    def cancel_controller(
        self,
        controller_id: str,
        url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Cancels the specified Controller instance.
        
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
                
            url (str):
                URL of the Controller instance. This parameter is required for a Controller cluster.
                
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
        
        return cancel_controller_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url,
            audit_log=audit_log
        )
        
    def switchover_controller_cluster(
        self,
        controller_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Performs a switch-over to the standby node.
        
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
                
            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.
                
        Returns:
            bool: Returns `True` if the operation was successful, otherwise `False`.
            
        Raises:
            ValueError:
                If required arguments such as `controller_id` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return switchover_controller_cluster_action(
            context=self._ctx,
            controller_id=controller_id,
            audit_log=audit_log
        )
        
    def restart_controller(
        self,
        controller_id: str,
        url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Restarts a Controller instance.
        
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
            
            url (Optional[str]):
                URL of the Controller instance. This parameter is required for a Controller cluster.
            
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
        
        return restart_controller_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url,
            audit_log=audit_log
        )
    
    def terminate_controller(
        self,
        controller_id: str,
        url: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Terminates a Controller instance.
            
        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.
            
            url (Optional[str]):
                URL of the Controller instance. This parameter is required for a Controller cluster.
            
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
        
        return terminate_controller_action(
            context=self._ctx,
            controller_id=controller_id,
            url=url,
            audit_log=audit_log
        )
        

    