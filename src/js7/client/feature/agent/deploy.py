from typing import List, Optional

from ....model.public.client.common.audit_log import AuditLog
from ....client.context import Context

from ...action.agent.deploy_cluster_agents_action import deploy_cluster_agents_action
from ...action.agent.deploy_standalone_agents_action import deploy_standalone_agents_action
from ...action.agent.deploy_subagent_clusters_action import deploy_subagent_clusters_action

class Deploy:
    def __init__(self, context: Context):
        self._ctx = context
        
    def cluster_agents(
        self,
        controller_id: str, 
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deploy cluster agents to a controller.

        Args:
            controller_id (str):
                The ID of the controller to which the cluster agents
                should be deployed.

            agent_ids (List[str]):
                A collection of cluster agent IDs to be deployed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return deploy_cluster_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
        
    def standalone_agents(
        self,
        controller_id: str,
        agent_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deploy standalone agents to a controller.

        Args:
            controller_id (str):
                The ID of the controller to which the agents should be deployed.

            agent_ids (List[str]):
                A collection of standalone agent IDs to be deployed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return deploy_standalone_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids,
            audit_log=audit_log
        )
    
    def subagent_clusters(
        self,
        controller_id: str,
        subagent_cluster_ids: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Deploy subagent clusters to a controller.

        Args:
            controller_id (str):
                The ID of the controller to which the subagent clusters
                should be deployed.

            subagent_cluster_ids (List[str]):
                A collection of subagent cluster IDs to be deployed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return deploy_subagent_clusters_action(
            context=self._ctx,
            controller_id=controller_id,
            subagent_cluster_ids=subagent_cluster_ids,
            audit_log=audit_log
        )