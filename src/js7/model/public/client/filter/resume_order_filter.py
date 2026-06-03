from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel

from .element.workflow_id import WorkflowID
from .element.folder import Folder


class ResumeOrderFilter(BaseModel):
    order_ids: Optional[List[str]] = None
    """
    Specified the order ids which should be modified.
    If this parameter is specified then the parameters `workflow_ids`, folders and states where applicable are ignored.
    """
    
    workflow_ids: Optional[List[WorkflowID]] = None
    """
    Filtered response by a collection of workflows specified by its path and optional version
    If this parameter is specified the parameter `folders` where applicable are ignored.
    """
    
    folders: Optional[List[Folder]] = None
    """Limits the result to a collection of folders."""
    
    states: Optional[List[Literal["PENDING", "SCHEDULED", "SCHEDULED", "SCHEDULED", "SUSPENDED", "WAITING", "PROMPTING", "FAILED", "BLOCKED"]]] = None
    """Filtered all orders with states."""
    
    force: Optional[bool] = None
    """force execution of non-startable jobs after kill."""
    
    from_current_block: Optional[bool] = None
    """Orders get the position from the beginning of the current block. Orders that are on top level in their scope are resumed from the current position."""
    
    position: Optional[Union[List[Union[int, str]], str]] = None
    """The position can also be specified by the label of the instruction."""
    
    variables: Optional[Dict[str, Any]] = None
    """
    Variables can only be set for resumimg a single order that position is not at the beginning of its workflow's scope.
    Otherwise an error is raised.
    It change the returned variables of the previous jobs.
    An object with key-value pairs. The value can be a string, number or boolean.
    """

    cycle_end_time: Optional[int] = None
    """A relative cycle end time in seconds."""