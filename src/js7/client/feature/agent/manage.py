from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from js7.model.public.client.common.store_agents import StoreAgent, StoreClusterAgent, StoreSubagent, SubagentCluster

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.agent.confirm_node_loss_agent_action import confirm_node_loss_agent_action
from ...action.agent.export_agents_action import export_agents_action
from ...action.agent.get_agents_status_action import get_agents_status_action
from ...action.agent.store_cluster_agents_action import store_cluster_agents_action
from ...action.agent.store_standalone_agents_action import store_standalone_agents_action
from ...action.agent.store_subagent_clusters_action import store_subagent_clusters_action
from ...action.agent.store_subagents_action import store_subagents_action
from ...action.agent.import_agents_action import import_agents_action


class Manage:
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
    
    def export_agents(
        self,
        out_path: Union[Path, str],
        agent_ids: List[str],
        archive_format: Literal['ZIP', 'TAR_GZ'] = "ZIP",
        audit_log: Optional[AuditLog] = None
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
        
        return export_agents_action(
            context=self._ctx,
            out_path=out_path,
            archive_format=archive_format,
            agent_ids=agent_ids,
            audit_log=audit_log
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
        audit_log: Optional[AuditLog]
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
        
    