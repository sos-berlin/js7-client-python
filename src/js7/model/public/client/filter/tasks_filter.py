from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel

from js7.model.public.client.filter.element.folder import Folder


class TasksFilter(BaseModel):
    date_from: Optional[datetime] = None
    """Filters items starting from a date."""
    
    date_to: Optional[datetime] = None
    """Filters items ending before a date."""
    
    completed_date_from: Optional[datetime] = None
    """Filters items starting from a date."""
    
    completed_date_to: Optional[datetime] = None
    """Filters items ending before a date."""
    
    job_name: Optional[str] = None
    """
    Limits result to a specified glob pattern of a Job name that supports '*' and '?' as wildcards where
    - '*' : match zero or more characters
    - '?' : match any single character
    """
    
    workflow_name: Optional[str] = None
    """
    Limits result to a specified glob pattern of a Workflow name that supports '*' and '?' as wildcards where
    - '*' : match zero or more characters
    - '?' : match any single character
    """
    
    workflow_paths: Optional[str] = None
    """
    Limits result to a specified glob pattern of a Workflow path that supports '*' and '?' as wildcards where
    - '*' : match zero or more characters
    - '?' : match any single character
    """
    
    folders: Optional[List[Folder]] = None
    """Limits the result to a collection of folders."""
    
    history_states: Optional[List[Literal["FAILED", "INCOMPLETE", "SUCCESSFUL"]]] = None
    """Limits result to specified states."""
    
    criticalities: Optional[List[Literal["CRITICAL", "NORMAL"]]] = None
    """Possible values are NORMAL and NORMAL Only records with these criticalities are responsed."""

