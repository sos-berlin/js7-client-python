from typing import List, Literal, Optional, Tuple
from pydantic import BaseModel


class StoreSubagent(BaseModel):
    id: str
    """
    The `id` is the name that is used in the Controller to identify a Subagent.
    This value is set once and cannot be overwritten.
    """
    
    url: str
    """URL of the subagent."""
    
    title: Optional[str] = None
    """The title of the agent."""
    
    director_type: Optional[Literal["NO_DIRECTOR", "PRIMARY_DIRECTOR", "SECONDARY_DIRECTOR"]] = None
    
    order: Optional[int] = None
    
    with_generate_subagent_cluster: bool = False
    """
    if true then a subagent cluster with only the subagent as member is created.
    The subagent cluster ID is equal the subagend ID.
    """


class StoreClusterAgent(BaseModel):
    id: str
    """
    The `id` is the (technical) name that is used in the Controller to identify an Agent.
    This value is set once and cannot be overwritten.
    """
    
    name: str
    """The `name` is the (logical) name that is used for the configuration of a Job to identify an Agent."""
    
    aliases: Optional[List[str]] = None
    """Aliases of the `name`."""
    
    title: Optional[str] = None
    """The title of the agent."""
    
    process_limit: Optional[int] = None
    """Limits the number max. processes that are started by the Agent."""
    
    subagents: List[StoreSubagent]


class StoreAgent(BaseModel):
    id: str
    """
    The `id` is the (technical) name that is used in the Controller to identify an Agent.
    This value is set once and cannot be overwritten.
    """
    
    name: str
    """The `name` is the (logical) name that is used for the configuration of a Job to identify an Agent."""
    
    aliases: Optional[List[str]] = None
    """Aliases of the `name`."""
    
    url: str
    """URL of the agent."""
    
    process_limit: Optional[int] = None
    """Limits the number max. processes that are started by the Agent."""
    
    hidden: bool = False
    """A hidden Agent will not be offered in JOC Cockpit during the Job configuration."""
    
    
class SubagentCluster(BaseModel):
    id: str
    """
    The `id` is the (technical) name that is used in the Controller to identify an Agent.
    This value is set once and cannot be overwritten.
    """
    
    subagent_cluster_id: str
    """The ID of the Subagent Cluster."""
    
    title: Optional[str] = None
    """A title of the Subagent Cluster."""
    
    subagent_ids: Optional[List[Tuple[str, int]]] = None
    """
    Collection of Subagents.
    
    Arguments:
        str: The subagent id.
        int: The subagent priority.
    """
    
    