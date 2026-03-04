from datetime import date, datetime
from typing import List, Literal, Optional
from pydantic import BaseModel

from .element.folder import Folder


class DailyPlanOrdersFilter(BaseModel):
    """
    Following elements filter the orders that should be considered.
    All filter elements will be combined with "and".
    The elements in the lists schedulePaths, scheduleFolders, workflowPaths, workflowFolders and controllerIds 
    will be combined with "or".
    """
    
    date_from: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The begin of the day range of the daily plan. 
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    date_to: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The end of the day range of the daily plan.
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    order_ids: Optional[List[str]] = None
    """Filters all orders in the given daily plan that have one of the order IDs in the given list of `order_ids`."""
    
    workflow_paths: Optional[List[str]] = None
    """Filters all orders in the given daily plan range that are assigned to one of the given workflows in `workflow_paths`."""
    
    workflow_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule assigned to a workflow
    located in one of the given folders. Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    schedule_paths: Optional[List[str]] = None
    """
    Filters all orders in the given daily plan range that have been generated with one of the given schedules in `schedule_paths`.
    """
    
    schedule_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule located in one of the given folders.
    Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    workflow_tags: Optional[List[str]] = None
    """Tags to be assigned to workflows."""
    
    order_tags: Optional[List[str]] = None
    """Tags to be assigned to orders."""
    
    controller_ids: Optional[List[str]] = None
    """Filters orders that have been generated for the Controller IDs that are in the list `controller_ids`."""
    
    states: Optional[List[Literal["PLANNED", "SUBMITTED", "FINISHED"]]] = None
    """Filters all orders that have one of the states specified in this list of states."""
    
    late: bool = False
    """If true filters all orders that are late. Late means that the current time is after the planned time+2 minutes."""


class DailyPlanCancelOrdersFilter(BaseModel):
    """
    Following elements filter the orders that should be considered.
    All filter elements will be combined with "and".
    The elements in the lists schedulePaths, scheduleFolders, workflowPaths, workflowFolders and controllerIds 
    will be combined with "or".
    """
    
    date_from: Optional[datetime] = None
    """
    The value has to have the format YYYY-MM-DD. The begin of the day range of the daily plan. 
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    date_to: Optional[datetime] = None
    """
    The value has to have the format YYYY-MM-DD. The end of the day range of the daily plan.
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    order_ids: Optional[List[str]] = None
    """Filters all orders in the given daily plan that have one of the order IDs in the given list of `order_ids`."""
    
    workflow_paths: Optional[List[str]] = None
    """Filters all orders in the given daily plan range that are assigned to one of the given workflows in `workflow_paths`."""
    
    workflow_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule assigned to a workflow
    located in one of the given folders. Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    schedule_paths: Optional[List[str]] = None
    """
    Filters all orders in the given daily plan range that have been generated with one of the given schedules in `schedule_paths`.
    """
    
    schedule_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule located in one of the given folders.
    Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    controller_ids: Optional[List[str]] = None
    """Filters orders that have been generated for the Controller IDs that are in the list `controller_ids`."""


class DailyPlanSubmitOrderFilter(BaseModel):
    date_from: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The begin of the day range of the daily plan. 
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    date_to: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The end of the day range of the daily plan.
    Depends on the settings for daily plan timezone and daily plan period.
    """

    schedule_paths: Optional[List[str]] = None
    """
    Filters all orders in the given daily plan range that have been generated with one of the given schedules in `schedule_paths`.
    """

    schedule_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule located in one of the given folders.
    Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    workflow_paths: Optional[List[str]] = None
    """Filters all orders in the given daily plan range that are assigned to one of the given workflows in `workflow_paths`."""
    
    workflow_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule assigned to a workflow
    located in one of the given folders. Depending on the value for `recursive` in one of the subfolders recursively too.
    """

    controller_ids: Optional[List[str]] = None
    """Filters orders that have been generated for the Controller IDs that are in the list `controller_ids`."""

    order_ids: Optional[List[str]]
    """Filters all orders in the given daily plan that have one of the order IDs in the given list of `order_ids`."""

    submission_history_ids: Optional[List[int]] = None
    """
    Filters all orders in the given daily plan range that have been generated by one of the given submissions. 
    To retrieve submissionHistoryIds call /dailyplan/submissions. 
    A submission can be manually executed or the automatically executed by the daily plan service.
    """
    
class DailyPlanDeleteOrdersFilter(BaseModel):
    date_from: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The begin of the day range of the daily plan. 
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    date_to: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The end of the day range of the daily plan.
    Depends on the settings for daily plan timezone and daily plan period.
    """

    schedule_paths: Optional[List[str]] = None
    """
    Filters all orders in the given daily plan range that have been generated with one of the given schedules in `schedule_paths`.
    """

    schedule_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule located in one of the given folders.
    Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    workflow_paths: Optional[List[str]] = None
    """Filters all orders in the given daily plan range that are assigned to one of the given workflows in `workflow_paths`."""
    
    workflow_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule assigned to a workflow
    located in one of the given folders. Depending on the value for `recursive` in one of the subfolders recursively too.
    """

    controller_ids: Optional[List[str]] = None
    """Filters orders that have been generated for the Controller IDs that are in the list `controller_ids`."""
    
    order_ids: Optional[List[str]]
    """Filters all orders in the given daily plan that have one of the order IDs in the given list of `order_ids`."""
    
    late: bool = False
    """If true filters all orders that are late. Late means that the current time is after the planned time+2 minutes."""
    
    submission_history_ids: Optional[List[int]] = None
    """
    Filters all orders in the given daily plan range that have been generated by one of the given submissions. 
    To retrieve submissionHistoryIds call /dailyplan/submissions. 
    A submission can be manually executed or the automatically executed by the daily plan service.
    """
    
    
class DailyPlanProjectionsFilter(BaseModel):
    """
    Filters all orders in the given daily plan range that have been generated by one of the given submissions. 
    To retrieve submissionHistoryIds call /dailyplan/submissions. 
    A submission can be manually executed or the automatically executed by the daily plan service.
    """

    date_from: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The begin of the day range of the daily plan. 
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    date_to: Optional[date] = None
    """
    The value has to have the format YYYY-MM-DD. The end of the day range of the daily plan.
    Depends on the settings for daily plan timezone and daily plan period.
    """
    
    schedule_paths: Optional[List[str]] = None
    """
    Filters all orders in the given daily plan range that have been generated with one of the given schedules in `schedule_paths`.
    """
    
    schedule_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule located in one of the given folders.
    Depending on the value for `recursive` in one of the subfolders recursively too.
    """
    
    workflow_paths: Optional[List[str]] = None
    """Filters all orders in the given daily plan range that are assigned to one of the given workflows in `workflow_paths`."""
    
    workflow_folders: Optional[List[Folder]] = None
    """
    Filters all orders in the given daily plan range that have been generated with a schedule assigned to a workflow
    located in one of the given folders. Depending on the value for `recursive` in one of the subfolders recursively too.
    """

    without_start_time: bool = False
    """If true, the workflows that have a start time for a day are considered. With false it is the other way round."""
    
    controller_ids: Optional[List[str]] = None
    """Filters orders that have been generated for the Controller IDs that are in the list `controller_ids`."""
    
    