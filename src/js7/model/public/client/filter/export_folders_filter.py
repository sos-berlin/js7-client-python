from typing import List, Optional, Union
from pydantic import BaseModel

from ..enum.object_types import DeployObjectType, ReleaseObjectType


class ExportFoldersFilter(BaseModel):
    folder_paths: List[str]
    """Paths of the inventory directories that should be exported."""
    
    use_short_path: bool = False
    """
    Determines if the desired objects are exported to the archive with a shortened path, e.g. 
    if set to `True` the object `/a/b/c/myWorkflow` will be exported as `/c/myWorkflow`.
    """
    
    recursive: bool = True
    """A switch to determine if the specified folders should be read recursively."""
    
    for_signing: bool
    
    object_types: Optional[List[Union[DeployObjectType, ReleaseObjectType]]] = None
    
    no_draft: bool = False
    """Determines if draft configurations are excluded from export."""
    
    no_deployed: bool = False
    """Determines if already deployed configurations are excluded from export."""
    
    no_released: bool = False
    """Determines if already released configurations are excluded from export."""
    
    no_invalid: bool = False
    """Determines if invalid draft configurations are excluded from export."""