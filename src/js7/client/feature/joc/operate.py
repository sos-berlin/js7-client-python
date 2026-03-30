from typing import Literal, Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.joc.switch_over_action import switch_over_action
from ...action.joc.run_service_action import run_service_action
from ...action.joc.restart_service_action import restart_service_action
from ...action.joc.restart_proxies_action import restart_proxies_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
    
    def switch_over(self, controller_id: str) -> bool:
        """
        Switch to an inactive JOC cluster member.

        Args:
            controller_id (str):
                The ID of the controller whose JOC cluster
                should perform the switchover.

        Returns:
            bool:
                Returns `True` if the switchover was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the switchover fails or the server version
                is incompatible.
        """
        
        return switch_over_action(context=self._ctx, controller_id=controller_id)
    
    def run_service(
        self,
        service_type: Literal["cleanup", "dailyplan"],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Run a JOC service immediately.

        Supported services include:
        - "cleanup"
        - "dailyplan"

        Args:
            service_type (Literal["cleanup", "dailyplan"]):
                The type of service to be executed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the service was successfully started,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the service execution fails or the server version
                is incompatible.
        """
    
        return run_service_action(
            context=self._ctx,
            service_type=service_type,
            audit_log=audit_log
        )
        
    def restart_service(
        self, 
        service_type: Literal["cleanup", "cluster", "dailyplan", "history", "lognotification", "monitor"],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Restart a JOC service.

        Supported services include:
        - "cleanup"
        - "cluster"
        - "dailyplan"
        - "history"
        - "lognotification"
        - "monitor"

        Args:
            service_type (Literal["cleanup", "cluster", "dailyplan", "history", "lognotification", "monitor"]):
                The type of service to be restarted.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the service was successfully restarted,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the restart operation fails or the server version
                is incompatible.
        """
        
        return restart_service_action(
            context=self._ctx,
            service_type=service_type,
            audit_log=audit_log
        )
    
    def restart_proxies(self, audit_log: Optional[AuditLog] = None) -> bool:
        """
        Restart proxy instances for all registered controllers.

        Args:
            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the proxy instances were successfully restarted,
                otherwise `False`.

        Raises:
            RuntimeError:
                If the restart operation fails or the server version
                is incompatible.
        """
        
        return restart_proxies_action(
            context=self._ctx,
            audit_log=audit_log
        )
        