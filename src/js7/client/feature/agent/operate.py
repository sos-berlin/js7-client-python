from typing import List, Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.agent.reset_agents_action import reset_agents_action
from ...action.agent.reset_subagent_action import reset_subagent_action
from ...action.agent.switchover_agent_action import switchover_agent_action
from ...action.agent.confirm_node_loss_agent_action import confirm_node_loss_agent_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
        
    def confirm_node_loss_agent(
        self,
        controller_id: str,
        agent_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Confirm the loss of an agent for a controller operating in cluster mode.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            agent_id (str):
                The ID of the agent whose loss should be confirmed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return confirm_node_loss_agent_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_id=agent_id,
            audit_log=audit_log
        )
        
    def reset_subagent(
        self,
        controller_id: str,
        subagent_id: str,
        force: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Reset a subagent at the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            subagent_id (str):
                The ID of the subagent to be reset.

            force (bool):
                If `True`, forces the reset even if validation checks
                would normally prevent the operation. Defaults to `False`.

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
        
        return reset_subagent_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_id=subagent_id,
            force=force,
            audit_log=audit_log
        )
        
    def switchover_agent(
        self,
        controller_id: str,
        agent_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Perform a switchover of the specified agent for a controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            agent_id (str):
                The ID of the agent to be switched over.

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

        return switchover_agent_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_id=agent_id,
            audit_log=audit_log
        )
        
    def reset_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        force: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Reset agents at the specified controller.

        Any currently running orders continue execution.
        Workflows and other deployable objects are withdrawn.
        The agents drop their journals and restart.
        Afterward, the controller attempts to reconnect to the agents,
        redeploy workflows and related objects, and resubmit orders.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            agent_ids (List[str]):
                A list of agent IDs to be reset.

            force (bool):
                If `True`, forces the reset.

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
        
        return reset_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            force=force,
            audit_log=audit_log
        )