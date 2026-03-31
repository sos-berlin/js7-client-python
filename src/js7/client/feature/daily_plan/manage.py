from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from ....client.context import Context
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.public.client.filter.element.folder import Folder
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.cycle import Cycle
from ....model.public.client.filter.daily_plan_order_filters import (
    DailyPlanOrdersFilter,  
    DailyPlanProjectionsFilter
)

from ...action.daily_plan.get_orders_action import get_orders_action
from ...action.daily_plan.copy_orders_action import copy_orders_action
from ...action.daily_plan.recreate_projections_action import recreate_projections_action
from ...action.daily_plan.get_calendar_projections_action import get_calendar_projections_action
from ...action.daily_plan.get_projection_dates_action import get_projection_dates_action
from ...action.daily_plan.modify_orders_action import modify_orders_action
from ...action.daily_plan.generate_orders_action import generate_orders_action
from ...action.daily_plan.delete_submissions_action import delete_submissions_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
        
    def get_orders(self, filter: DailyPlanOrdersFilter) -> Dict[str, Any]:
        """
        Retrieves orders for a specified daily plan interval.

        Args:
            filter (DailyPlanOrdersFilter):
                Defines the filter criteria used to select orders
                from the daily plan interval.

        Returns:
            Dict ([str, Any]):
                A dictionary containing the orders matching the
                specified daily plan filter.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """

        return get_orders_action(
            context=self._ctx,
            filter=filter
        )
        
    def copy_orders(
        self,
        controller_id: str,
        order_ids: List[str],
        scheduled_for: Optional[ScheduleTime] = None,
        cycle: Optional[Cycle] = None,
        force_job_admission: bool = False,
        sticky_daily_plan_date: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> List[Tuple[str, str]]:
        """
        Copy orders.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            order_ids (List[str]):
                A list of order IDs to be copied.

            scheduled_for (Optional[ScheduleTime]):
                Specifies the time for which the copied orders should be scheduled.

            cycle (Optional[Cycle]):
                Defines the cycle for cyclic orders, including the begin date,
                end date, and repeat interval.

            force_job_admission (bool):
                If True, any job admission times defined in job instructions
                will be ignored.

            sticky_daily_plan_date (bool):
                If True, the copied orders will retain their original Daily Plan date.

            audit_log (Optional[AuditLog]):
                Optional audit log information to include with the request.

        Returns:
            List (Tuple[str, str]):
                A list of tuples in the format `(old_id, new_id)`, mapping the
                original order ID to the newly created order ID.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return copy_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            scheduled_for=scheduled_for,
            cycle=cycle,
            force_job_admission=force_job_admission,
            sticky_daily_plan_date=sticky_daily_plan_date,
            audit_log=audit_log
        )
        
    def recreate_projections(self) -> bool:
        """
        (Re)creates daily plan projections.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return recreate_projections_action(context=self._ctx)
    
    def get_calendar_projections(self, filter: DailyPlanProjectionsFilter) -> Dict[str, Any]:
        """
        Retrieve the daily plan projection dates that include start times.

        Args:
            filter (DailyPlanProjectionsFilter):
                Defines the criteria used to filter the projection entries.

        Returns:
            Dict ([str, Any]):
                A dictionary containing the JSON representation of the years.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return get_calendar_projections_action(
            context=self._ctx,
            filter=filter
        )
        
    def get_projection_dates(self, filter: DailyPlanProjectionsFilter) -> Dict[str, Any]:
        """
        Retrieve the start times for a date range of daily plan projections.

        Args:
            filter (DailyPlanProjectionsFilter):
                Defines the criteria used to filter the projection entries.

        Returns:
            Dict ([str, Any]):
                A dictionary containing the JSON representation of the years.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return get_projection_dates_action(
            context=self._ctx,
            filter=filter
        )
        
    def modify_orders(
        self,
        controller_id: str,
        order_ids: List[str],
        scheduled_for: Optional[ScheduleTime] = None,
        cycle: Optional[Cycle] = None,
        force_job_admission: bool = False,
        sticky_daily_plan_date: bool = False,
        variables: Optional[Dict[str, Any]] = None,
        remove_variables: Optional[List[str]] = None,
        start_position_label: Optional[str] = None,
        end_position_labels: Optional[List[str]] = None,
        block_position_label: Optional[str] = None,
        audit_log: Optional[AuditLog] = None
    ) -> List[Tuple[str, str]]:
        """
        Modify orders in the daily plan.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            order_ids (List[str]):
                The IDs of the orders to be modified.

            scheduled_for (Optional[ScheduleTime]):
                Adjusts the start time of the orders.

            cycle (Optional[Cycle]):
                Defines the cycle for cyclic orders, including the begin date,
                end date, and repeat interval.

            force_job_admission (bool):
                If True, any job admission times defined in job instructions
                will be ignored.

            sticky_daily_plan_date (bool):
                If True, the orders will retain their original Daily Plan date.

            variables (Optional[Dict[str, Any]]):
                A dictionary of key-value pairs to be set for the orders.
                Values may be strings, numbers, or booleans.
                Existing variables will be updated with the new values.
                Non-existing variables will be added.
                To remove variables, use the `remove_variables` parameter.

            remove_variables (Optional[List[str]]):
                A list of variable keys to be removed from the orders.

            start_position_label (Optional[str]):
                By default, an order starts with its first instruction.
                This parameter specifies the label of the instruction
                from which the order should start.

            end_position_labels (Optional[List[str]]):
                Specifies one or more instruction labels at which the order
                should end.

            block_position_label (Optional[str]):
                Restricts the order execution to the specified block instruction,
                identified by its label.

            audit_log (Optional[AuditLog]):
                Optional audit log information to include with the request.

        Returns:
            List (Tuple[str, str]):
                A list of tuples in the format (old_id, new_id), mapping the
                original order ID to the modified order ID.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return modify_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            scheduled_for=scheduled_for,
            cycle=cycle,
            force_job_admission=force_job_admission,
            sticky_daily_plan_date=sticky_daily_plan_date,
            variables=variables,
            remove_variables=remove_variables,
            start_position_label=start_position_label,
            end_position_labels=end_position_labels,
            block_position_label=block_position_label,
            audit_log=audit_log
        )
        
    def generate_orders(
        self,
        controller_id: str,
        daily_plan_dates: List[date],
        schedule_folder_paths: Optional[List[Folder]] = None,
        schedule_paths: Optional[List[str]] = None,
        workflow_folder_paths: Optional[List[Folder]] = None,
        workflow_paths: Optional[List[str]] = None,
        overwrite: bool = False,
        with_submit: bool = False,
        include_non_auto_planned_orders: bool = False,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Generate orders for the specified daily plans.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            daily_plan_dates (List[date]):
                The dates of the daily plans for which orders should be generated.

            schedule_folder_paths (Optional[List[Folder]]):
                Generates orders for the specified daily plans based on the schedules
                located in the given folder(s).

            schedule_paths (Optional[List[str]]):
                Generates orders for the specified daily plans based on the
                explicitly selected schedule(s).

            workflow_folder_paths (Optional[List[Folder]]):
                Generates orders for the specified daily plans based on the schedules
                assigned to workflows located in the given folder(s).

            workflow_paths (Optional[List[str]]):
                Generates orders for the specified daily plans based on the schedules
                assigned to the explicitly selected workflow(s).

            overwrite (bool):
                If True, existing orders (same workflow, same start time, same schedule name)
                will be overwritten. Any variables will also be overwritten.

            with_submit (bool):
                If True, the generated orders will be submitted to the Controller.
                If False, the orders will only be planned and not submitted.

            include_non_auto_planned_orders (bool):
                If True, all orders will be planned.
                If False, only orders with automatic planning enabled in the
                corresponding schedule will be planned.

            audit_log (Optional[AuditLog]):
                Optional audit log information to include with the request.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return generate_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            daily_plan_dates=daily_plan_dates,
            schedule_folder_paths=schedule_folder_paths,
            schedule_paths=schedule_paths,
            workflow_folder_paths=workflow_folder_paths,
            workflow_paths=workflow_paths,
            overwrite=overwrite,
            with_submit=with_submit,
            include_non_auto_planned_orders=include_non_auto_planned_orders,
            audit_log=audit_log
        )
        
    def delete_submissions(
        self,
        controller_id: str,
        filter_date_for: Optional[date] = None,
        filter_date_from: Optional[date] = None,
        filter_date_to: Optional[date] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Delete daily plan submissions.

        Args:
            controller_id (str):
                The ID of the controller on which the operation will be executed.

            filter_date_for (Optional[date]):
                Specifies the exact daily plan date for which submissions
                should be deleted.

            filter_date_from (Optional[date]):
                Defines the start date of the interval used to search
                for submissions.

            filter_date_to (Optional[date]):
                Defines the end date of the interval used to search
                for submissions.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return delete_submissions_action(
            context=self._ctx,
            controller_id=controller_id,
            filter_date_for=filter_date_for,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            audit_log=audit_log
        )
        
    