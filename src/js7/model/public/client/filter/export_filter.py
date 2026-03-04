from typing import List, Optional, Union
from pydantic import BaseModel, model_validator

from ..common.configurations import DraftConfiguration, DeployConfiguration, ReleaseConfiguration


class ExportFilter(BaseModel):
    use_short_path: Optional[bool] = None
    """Determines if the desired objects are exported to the archive with a shortened path, e.g. if set to true the object /a/b/c/myWorkflow will be exported as /c/myWorkflow."""
    
    start_folder: Optional[str] = None
    """
    The path given determines the starting point for the relative path. E.g. `start_folder` /a/b/c results in objects starting with 
    relative path c/... in the exported archive. Only used in conjunction with `use_short_path`.
    """
    
    include_all_tags: Optional[bool] = None
    """If false then only Tags and Tag Groups assigned the exported scheduling objects will be added to the export file."""
    
    for_signing: bool
    """
    Controls the export mode.

    - `True`: Signing mode — only deployable objects are exported and prepared for cryptographic signing.
    - `False`: Shallow copy mode — both releasable and deployable objects are included in the export.
    """
    
    without_invalid_drafts: Optional[bool] = None
    """Decides if invalid draft objects are excluded from export."""
    
    configurations: List[Union[DraftConfiguration, DeployConfiguration, ReleaseConfiguration]]
    
    @model_validator(mode="after")
    def validate_configurations(self):
        # Validate: for_signing
        if self.for_signing:
            for c in self.configurations:
                if not isinstance(c, (DeployConfiguration, DraftConfiguration)):
                    raise ValueError(
                        "When 'for_signing' is set to True, only DeployConfiguration and DraftConfiguration objects are supported."
                    )
        # Validate: shallow_copy
        else:
            for c in self.configurations:
                if not isinstance(c, (DeployConfiguration, ReleaseConfiguration)):
                    raise ValueError(
                        "When 'for_signing' is set to False (shallow copy mode), only DeployConfiguration and ReleaseConfiguration objects are supported."
                    )

        return self
        
    