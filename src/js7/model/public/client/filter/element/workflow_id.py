from typing import Optional
from pydantic import BaseModel


class WorkflowID(BaseModel):
    workflow_path: str
    """Specifies the path of a workflow."""
    
    version_id: Optional[str] = None
    """Optional, string	Field to specify the version of a workflow."""