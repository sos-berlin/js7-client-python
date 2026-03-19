from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.store_agents import StoreAgent, StoreClusterAgent, StoreSubagent, SubagentCluster

from ...action.agent.disable_standalone_agents_action import disable_standalone_agents_action
from ...action.agent.disable_subagents_action import disable_subagents_action
from ...action.agent.enable_subagents_action import enable_subagents_action
from ...action.agent.enable_standalone_agents_action import enable_standalone_agents_action
from ...action.agent.export_agents_action import export_agents_action
from ...action.agent.get_agents_status_action import get_agents_status_action
from ...action.agent.store_cluster_agents_action import store_cluster_agents_action
from ...action.agent.store_standalone_agents_action import store_standalone_agents_action
from ...action.agent.store_subagent_clusters_action import store_subagent_clusters_action
from ...action.agent.store_subagents_action import store_subagents_action
from ...action.agent.import_agents_action import import_agents_action
from ...action.agent.delete_subagent_action import delete_subagent_action
from ...action.agent.delete_subagent_clusters_action import delete_subagent_clusters_action
from ...action.agent.remove_agent_action import remove_agent_action
from ...action.agent.revoke_cluster_agents_action import revoke_cluster_agents_action
from ...action.agent.revoke_standalone_agents_action import revoke_standalone_agents_action
from ...action.agent.revoke_subagent_clusters_action import revoke_subagent_clusters_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
    
    def export_agents(
        self,
        out_path: Union[Path, str],
        agent_ids: List[str],
        archive_format: Literal['ZIP', 'TAR_GZ'] = "ZIP"
    ) -> bool:
        """
        Export the specified agents to an archive file.

        Args:
            out_path (Union[Path, str]):
                The target path where the archive file will be created.

            agent_ids (List[str]):
                A list of agent IDs to be exported.

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format to be created. Defaults to "ZIP".

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
        
        return export_agents_action(
            context=self._ctx,
            out_path=out_path,
            archive_format=archive_format,
            agent_ids=agent_ids
        )
        
    def get_agents_status_info(
        self,
        controller_id: str,
        agent_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Retrieve status information for the specified agents of a controller.

        Args:
            controller_id (str):
                The ID of the controller whose agents should be queried.

            agent_ids (List[str]):
                A list of agent IDs for which status information should be retrieved.

        Returns:
            Dict[str, Any]:
                A dictionary containing the JSON representation of the response
                with the agents' status information.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return get_agents_status_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_ids=agent_ids
        )

    def store_cluster_agents(
        self,
        controller_id: str,
        agents: List[StoreClusterAgent],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store cluster agents for the specified controller.

        Args:
            controller_id (str):
                The ID of the controller to which the cluster agents
                should be stored.

            agents (List[StoreClusterAgent]):
                A list of cluster agent definitions to be stored.

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
        
        return store_cluster_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agents=agents,
            audit_log=audit_log
        )
    
    def store_standalone_agents(
        self,
        controller_id: str,
        agents: List[StoreAgent],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store standalone agents for the specified controller.

        Args:
            controller_id (str):
                The ID of the controller to which the standalone agents
                should be stored.

            agents (List[StoreAgent]):
                A list of standalone agent definitions to be stored.

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
        
        return store_standalone_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            agents=agents,
            audit_log=audit_log
        )
        
    def store_subagent_clusters(
        self,
        subagent_clusters: List[SubagentCluster],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store subagent clusters.

        Args:
            subagent_clusters (List[SubagentCluster]):
                A list of subagent cluster definitions to be stored.

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
        
        return store_subagent_clusters_action(
            context=self._ctx,
            subagent_clusters=subagent_clusters,
            audit_log=audit_log
        )
        
    def store_subagents(
        self,
        controller_id: str,
        agent_id: str,
        subagents: List[StoreSubagent],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Store subagents for the specified agent of a controller.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            agent_id (str):
                The ID of the agent to which the subagents belong.

            subagents (List[StoreSubagent]):
                A list of subagent definitions to be stored.

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
        
        return store_subagents_action(
            context=self._ctx,
            controller_id=controller_id,
            agent_id=agent_id,
            subagents=subagents,
            audit_log=audit_log
        )
        
    def import_agents(
        self,
        controller_id: str,
        file_path: Union[Path, str],
        archive_format: Literal["ZIP", "TAR_GZ"],
        overwrite: bool,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Imports agent configurations.

        Supported inputs:
        - ZIP or TAR.GZ archives ('.zip', '.tar.gz', '.tgz').
        If a directory contains multiple archives, all archives are processed recursively.
        - Directories containing '.json' configuration files (processed recursively).
        - A single '.json' configuration file.

        Args:
            controller_id (str):
                The ID of the controller to which the agent configuration
                should be imported.

            file_path (Union[Path, str]):
                The local path to the file or directory to be imported.

            archive_format (Literal["ZIP", "TAR_GZ"]):
                The archive format to be created by the client.
                This does not refer to the local format specified by `file_path`.

            overwrite (bool):
                If True, agent configurations from the import archive
                will overwrite existing agents.

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
        
        return import_agents_action(
            context=self._ctx,
            controller_id=controller_id,
            file_path=file_path,
            archive_format=archive_format,
            overwrite=overwrite,
            audit_log=audit_log
        )
    
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
    