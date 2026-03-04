from typing import Optional
from pydantic import BaseModel, model_validator

from ..enum.object_types import DeployObjectType, ReleaseObjectType, ObjectType


class _BaseConfiguration(BaseModel):
    path: str
    """Path to an inventory object or folder."""


class DeployConfiguration(_BaseConfiguration):
    commit_id: Optional[str] = None
    """Optional commit identifier used to deploy a specific inventory state."""
    
    object_type: DeployObjectType
    """Type of the deployable inventory object."""
    
    recursive: bool = False
    """If set to True and `path` refers to a folder, all contained objects are processed recursively."""


class DraftConfiguration(_BaseConfiguration):
    object_type: DeployObjectType
    """Type of the draft inventory object."""
    
    recursive: bool = False
    """If set to True and `path` refers to a folder, all contained objects are processed recursively."""
    
    @model_validator(mode="after")
    def validate_recursive(self):
        if self.recursive and self.object_type != "FOLDER":
            raise ValueError("'recursive' can only be used when object_type is 'FOLDER'.")
        return self
    
    
class ReleaseConfiguration(_BaseConfiguration):
    object_type: ReleaseObjectType
    """Type of the releasable inventory object."""
    
    recursive: bool = False
    """If set to True and `path` refers to a folder, all contained objects are processed recursively."""

    @model_validator(mode="after")
    def validate_recursive(self):
        if self.recursive and self.object_type != "FOLDER":
            raise ValueError("'recursive' can only be used when object_type is 'FOLDER'.")
        return self


class Configuration(_BaseConfiguration):
    object_type: ObjectType
    """Type of the inventory object."""
