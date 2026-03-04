from typing import List, Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.agent.delete_subagent_action import delete_subagent_action
from ...action.agent.delete_subagent_clusters_action import delete_subagent_clusters_action
from ...action.agent.disable_standalone_agents_action import disable_standalone_agents_action
from ...action.agent.disable_subagents_action import disable_subagents_action
from ...action.agent.enable_standalone_agents_action import enable_standalone_agents_action
from ...action.agent.enable_subagents_action import enable_subagents_action
from ...action.agent.reset_agents_action import reset_agents_action
from ...action.agent.reset_subagent_action import reset_subagent_action
from ...action.agent.switchover_agent_action import switchover_agent_action
from ...action.agent.remove_agent_action import remove_agent_action
from ...action.agent.revoke_cluster_agents_action import revoke_cluster_agents_action
from ...action.agent.revoke_standalone_agents_action import revoke_standalone_agents_action
from ...action.agent.revoke_subagent_clusters_action import revoke_subagent_clusters_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
        
    def delete_subagent(
        self,
        controller_id: str, 
        subagent_id: str,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Delete a subagent from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the subagent
                should be deleted.

            subagent_id (str):
                The ID of the subagent to be deleted.

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
        
        return delete_subagent_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_id=subagent_id,
            audit_log=audit_log
        )
        
    def delete_subagent_clusters(
        self,
        controller_id: str, 
        subagent_cluster_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Delete one or more subagent clusters from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the subagent clusters
                should be deleted.

            subagent_cluster_ids (List[str]):
                A list of subagent cluster IDs to be deleted.

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
        
        return delete_subagent_clusters_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_cluster_ids=subagent_cluster_ids,
            audit_log=audit_log
        )
        
    def disable_standalone_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Disable standalone agents at the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            agent_ids (List[str]):
                A list of standalone agent IDs to be disabled.

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
        
        return disable_standalone_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
        
    def disable_subagents(
        self,
        controller_id: str,
        subagent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Disable subagents at the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            subagent_ids (List[str]):
                A list of subagent IDs to be disabled.

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
        
        return disable_subagents_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_ids=subagent_ids,
            audit_log=audit_log
        )
        
    def enable_standalone_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Enable standalone agents at the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            agent_ids (List[str]):
                A list of standalone agent IDs to be enabled.

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
        
        return enable_standalone_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
    
    def enable_subagents(
        self,
        controller_id: str,
        subagent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Enable subagents at the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation
                will be executed.

            subagent_ids (List[str]):
                A list of subagent IDs to be enabled.

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
        
        return enable_subagents_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_ids=subagent_ids,
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
        
    def remove_agent(
        self,
        controller_id: str,
        agent_id: str,
        force: bool,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Remove an agent from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the agent should be removed.

            agent_id (str):
                The ID of the agent to be removed.

            force (bool):
                If `True`, forces the removal.

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
        
        return remove_agent_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_id=agent_id,
            force=force,
            audit_log=audit_log
        )
    
    def revoke_cluster_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Revoke cluster agents from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the cluster agents
                should be revoked.

            agent_ids (List[str]):
                A collection of cluster agent IDs to be revoked.

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
        
        return revoke_cluster_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
        
    def revoke_standalone_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Revoke standalone agents from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the standalone agents
                should be revoked.

            agent_ids (List[str]):
                A collection of standalone agent IDs to be revoked.

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
        
        return revoke_standalone_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
    
    def revoke_subagent_clusters(
        self,
        controller_id: str,
        subagent_cluster_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Revoke subagent clusters from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the subagent clusters
                should be revoked.

            subagent_cluster_ids (List[str]):
                A collection of subagent cluster IDs to be revoked.

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
        
        return revoke_subagent_clusters_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_cluster_ids=subagent_cluster_ids,
            audit_log=audit_log
        )