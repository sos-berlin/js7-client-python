from typing import Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.filter.daily_plan_order_filters import (
    DailyPlanCancelOrdersFilter, 
    DailyPlanSubmitOrderFilter, 
    DailyPlanDeleteOrdersFilter
)

from ...action.daily_plan.cancel_orders_action import cancel_orders_action
from ...action.daily_plan.submit_orders_action import submit_orders_action
from ...action.daily_plan.delete_orders_action import delete_orders_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
    
    def cancel_orders(self, filter: DailyPlanCancelOrdersFilter) -> bool:
        """
        Cancels submitted orders within a specified daily plan interval.

        Args:
            filter (DailyPlanCancelOrdersFilter):
                Defines the filter criteria used to select the orders
                to be canceled from the daily plan interval.

        Returns:
            bool:
                Returns `True` if the operation was successful.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return cancel_orders_action(
            context=self._ctx,
            filter=filter
        )
        
    def submit_orders(
        self,
        filter: DailyPlanSubmitOrderFilter,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Submit planned orders for a specified daily plan interval.

        Args:
            filter (DailyPlanSubmitOrderFilter):
                Defines the criteria used to select the orders to be submitted.
                All filter attributes are combined using a logical "AND".
                The elements within the lists `schedulePaths`, `scheduleFolders`,
                `workflowPaths`, `workflowFolders`, and `controllerIds` are
                each combined using a logical "OR".

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
        
        return submit_orders_action(
            context=self._ctx,
            filter=filter,
            audit_log=audit_log
        )
    
        
    def delete_orders(
        self, 
        filter: DailyPlanDeleteOrdersFilter,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Delete planned orders for a specified daily plan interval.

        Args:
            filter (DailyPlanDeleteOrdersFilter):
                Defines the criteria used to select the orders to be deleted.
                All filter attributes are combined using a logical "AND".
                The elements within the lists `schedulePaths`, `scheduleFolders`,
                `workflowPaths`, `workflowFolders`, and `controllerIds` are
                each combined using a logical "OR".

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
        
        return delete_orders_action(
            context=self._ctx,
            filter=filter,
            audit_log=audit_log
        )
