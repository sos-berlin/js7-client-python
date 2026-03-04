from typing import Any, Dict, List, Optional, Tuple

from ....client.context import Context
from ....model.public.client.common.schedule_time import ScheduleTime
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.cycle import Cycle
from ....model.public.client.filter.daily_plan_order_filters import (
    DailyPlanOrdersFilter,  
    DailyPlanProjectionsFilter
)

from ...action.daily_plan.get_orders_action import get_orders_action
from ...action.daily_plan.copy_orders_action import copy_orders_action
from ...action.daily_plan.create_projections_action import create_projections_action
from ...action.daily_plan.get_calendar_projections_action import get_calendar_projections_action
from ...action.daily_plan.get_projection_dates_action import get_projection_dates_action


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
        
    def create_projections(self) -> bool:
        """
        (Re)creates daily plan projections.

        Returns:
            bool:
                Returns True if the operation was successful.

        Raises:
            RuntimeError:
                If the server version is incompatible or if an unexpected
                response is returned.
        """
        
        return create_projections_action(context=self._ctx)
    
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