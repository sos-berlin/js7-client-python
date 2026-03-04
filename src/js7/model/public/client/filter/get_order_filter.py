from datetime import datetime
from typing import List, Literal, Optional, Union
from pydantic import BaseModel

from .element.folder import Folder
from .element.workflow_id import WorkflowID


class GetOrderFilter(BaseModel):
    order_ids: Optional[List[str]] = None
    """Filtered response by a collection of orderIds If this parameter is specified then parameters such as workflowIds, states, folders and regex where applicable are ignored."""

    workflow_ids: Optional[List[WorkflowID]] = None
    """
    Filtered response by a collection of workflows specified by its path and optional version If this parameter 
    is specified then parameters such as folders, states, regex and agentName where applicable are ignored.
    """
    
    order_tags: Optional[List[str]] = None
    
    folders: Optional[List[Folder]] = None
    """Limits the result to a collection of folders."""
    
    compact: bool = False
    """A compact response is returned if this parameter is 'true'."""
    
    regex: Optional[str] = None
    """Regular expression to filter the collection."""
    
    states: Optional[List[Literal["PENDING", "SCHEDULED", "SCHEDULED", "SCHEDULED", "SUSPENDED", "WAITING", "PROMPTING", "FAILED", "BLOCKED"]]] = None
    """Filtered all orders with states."""
    
    state_date_from: Optional[Union[str, datetime]] = None
    """
    Filters those orders whose current status is younger than the specified point in time.
    
    0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp.
    """
    
    state_date_to: Optional[Union[str, datetime]] = None
    """
    Filters those orders whose current status is older than the specified point in time.
    
    0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp.
    """
    
    date_to: Optional[datetime] = None
    """Filters Orders whose schedule is before a date."""
    
    timezone: Optional[str] = None
    """If this parameter is set then it beats the time offset of absolute dates in `date_to`."""
    
    limit: Optional[int] = None
    """Limits the number of resulting items, -1=unlimited."""
    
    without_workflow_tags: Optional[bool] = None
    """if true then response doesn't contain 'workflowsTagPerWorkflow'"""
    
    workflow_tags: Optional[List[str]] = None