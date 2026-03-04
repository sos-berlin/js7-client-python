from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

from js7.model.public.client.common.schedule_time import ScheduleTime

from ..enum.order_priority import OrderPriority


class PlanID(BaseModel):    
    notice_space_key: str
    """Schema ID of a plan, e.g. 'DailyPlan'."""
    
    plan_schema_id: str
    """Plan key of the plan."""


class Order(BaseModel):
    arguments: Optional[Dict[str, Any]] = None
    """An object with key-value pairs. The value can be a string, number or boolean."""

    block_position: Optional[Union[List[Union[int, str]], str]] = None
    """The order runs only inside the specified block instruction. The position can also be specified by the label of the block instruction."""
    
    end_positions: Optional[List[Union[List[Union[int, str]], str]]] = None
    """The order ends on one of these positions. The position can also be specified by the label of the instruction."""

    force_job_admission: bool = False
    """If true then any admission times at a Job instruction will be ignored."""
    
    open_closed_plan: bool = False
    """If true then a closed plan will be reopen automatically."""
    
    order_name: Optional[str]
    """`order_name` is only a part of the `order_id` in the form "#<date>#T<uniqueId>-<orderName>"."""
    
    plan_id: Optional[PlanID] = None
    
    priority: Optional[Union[OrderPriority, int]] = None
    """Priority of the order."""
    
    scheduled_for: Optional[ScheduleTime] = None
    """Sets the start time of the order execution."""

    start_position: Optional[Union[List[Union[int, str]], str]] = None
    """The order starts with the first instruction per default. The position can also be specified by the label of the instruction."""

    tags: Optional[List[str]] = None

    workflow_path: str
    """e. g. `/folder/my-workflow`"""