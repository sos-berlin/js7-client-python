from typing import List, Literal, Optional
from pydantic import BaseModel

from .element.folder import Folder

class OrderHistoryFilter(BaseModel):
    date_from: Optional[str] = None
    """
    The value has multiple formats
    - Filters items starting from a date.
    - an ISO 8601 date format with the time offset and milliseconds being optional, e.g.
        - YYYY-MM-DDThh:mm:ss[.s][Z (Z means +00)]
        - YYYY-MM-DDThh:mm:ss[.s][+01:00]
        - YYYY-MM-DDThh:mm:ss[.s][+0100]
        - YYYY-MM-DDThh:mm:ss[.s][+01]
    - a format for a period relative to the current time, e.g. 6h, 12h, 1d, 1w that specifies the quantity followed by a qualifier:
        - s (seconds)
        - m (minutes)
        - h (hours)
        - d (days)
        - w (weeks)
        - M (months)
        - y (years)
    - a time offset is optional (e.g. 2d+02:00)
        - it can also be specified with the parameter `timezone`
        - if `timezone` is undefined then UTC is used
    - the value 0 indicates the current time
    """
    
    date_to: Optional[str] = None
    """
    The value has multiple formats
    - Filters items starting from a date.
    - an ISO 8601 date format with the time offset and milliseconds being optional, e.g.
        - YYYY-MM-DDThh:mm:ss[.s][Z (Z means +00)]
        - YYYY-MM-DDThh:mm:ss[.s][+01:00]
        - YYYY-MM-DDThh:mm:ss[.s][+0100]
        - YYYY-MM-DDThh:mm:ss[.s][+01]
    - a format for a period relative to the current time, e.g. 6h, 12h, 1d, 1w that specifies the quantity followed by a qualifier:
        - s (seconds)
        - m (minutes)
        - h (hours)
        - d (days)
        - w (weeks)
        - M (months)
        - y (years)
    - a time offset is optional (e.g. 2d+02:00)
        - it can also be specified with the parameter `timezone`
        - if `timezone` is undefined then UTC is used
    - the value 0 indicates the current time
    """
    
    completed_date_from: Optional[str] = None
    """
    The value has multiple formats
    - Filters items starting from a date.
    - an ISO 8601 date format with the time offset and milliseconds being optional, e.g.
        - YYYY-MM-DDThh:mm:ss[.s][Z (Z means +00)]
        - YYYY-MM-DDThh:mm:ss[.s][+01:00]
        - YYYY-MM-DDThh:mm:ss[.s][+0100]
        - YYYY-MM-DDThh:mm:ss[.s][+01]
    - a format for a period relative to the current time, e.g. 6h, 12h, 1d, 1w that specifies the quantity followed by a qualifier:
        - s (seconds)
        - m (minutes)
        - h (hours)
        - d (days)
        - w (weeks)
        - M (months)
        - y (years)
    - a time offset is optional (e.g. 2d+02:00)
        - it can also be specified with the parameter `timezone`
        - if `timezone` is undefined then UTC is used
    - the value 0 indicates the current time
    """
    
    completed_date_to: Optional[str] = None
    """
    The value has multiple formats
    - Filters items starting from a date.
    - an ISO 8601 date format with the time offset and milliseconds being optional, e.g.
        - YYYY-MM-DDThh:mm:ss[.s][Z (Z means +00)]
        - YYYY-MM-DDThh:mm:ss[.s][+01:00]
        - YYYY-MM-DDThh:mm:ss[.s][+0100]
        - YYYY-MM-DDThh:mm:ss[.s][+01]
    - a format for a period relative to the current time, e.g. 6h, 12h, 1d, 1w that specifies the quantity followed by a qualifier:
        - s (seconds)
        - m (minutes)
        - h (hours)
        - d (days)
        - w (weeks)
        - M (months)
        - y (years)
    - a time offset is optional (e.g. 2d+02:00)
        - it can also be specified with the parameter `timezone`
        - if `timezone` is undefined then UTC is used
    - the value 0 indicates the current time
    - Filters items ending before a date
    """

    order_id: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match any single character."""
    
    workflow_name: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match any single character."""
    
    folders: Optional[List[Folder]] = None
    """Limits the result to a collection of folders."""
    
    history_states: Optional[List[Literal["FAILED", "INCOMPLETE", "SUCCESSFUL"]]] = None
    """Limits result to specified states."""

    limit: int = 10000
    """only for db history urls to restrict the number of responsed records; -1=unlimited."""
