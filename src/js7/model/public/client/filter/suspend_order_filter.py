from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel

from .element.workflow_id import WorkflowID
from .element.folder import Folder


class SuspendOrderFilter(BaseModel):
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
    
    date_from: Optional[datetime] = None
    """Filters items starting from a date."""
    
    date_to: Optional[datetime] = None
    """Filters items ending before a date."""
    
    timezone: Optional[str] = None
    """If this parameter is set then it beats the time offset in `date_from` and `date_to`."""
    
    reset: Optional[bool] = None
    """reset any instruction that is currently executed."""
    
    kill: Optional[bool] = None
    """without a signal(false) or with SIGTERM(true)."""
    
    deep: Optional[bool] = None
    """if true then child orders are also processed."""