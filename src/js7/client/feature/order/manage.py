from typing import Any, Dict, List, Optional, Tuple

from ...context import Context
from ....model.public.client.filter.order_history_filter import OrderHistoryFilter
from ....model.public.client.filter.get_order_filter import GetOrderFilter
from ....model.public.client.input.add_order import Order

from ...action.order.get_order_history_action import get_order_history_action
from ...action.order.get_orders_action import get_orders_action
from ...action.order.get_orders_overview_action import get_orders_overview_action
from ...action.order.get_order_log_action import get_order_log_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
        
    def get_order_history(self, controller_id: str, filter: OrderHistoryFilter) -> Dict[str, Any]:
        """
        Retrieve the order history for the specified controller.

        Args:
            controller_id (str):
                The ID of the controller whose order history
                should be retrieved.

            filter (OrderHistoryFilter):
                Defines the criteria used to filter the order history.

        Returns:
            Dict[str, Any]:
                A dictionary containing the order history data.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_order_history_action(
            context=self._ctx,
            controller_id=controller_id,
            filter=filter
        )
        
    def get_orders(self, controller_id: str, filter: GetOrderFilter) -> List[Order]:
        """
        Retrieve orders from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which the orders
                should be retrieved.

            filter (GetOrderFilter):
                Defines the criteria used to filter the orders,
                such as workflow path or order state.

        Returns:
            List[Order]:
                A list of matching order objects.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return get_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            filter=filter
        )

    def get_orders_overview(
        self,
        controller_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        Summary with number of successful and failed orders.
        
        Args:
            controller_id (Optional[str]):
                The ID of the controller from which the orders should be retrieved.

            date_from (Optional[str]):
                The value has multiple formats
                Filters items starting from a date.
                an ISO 8601 date format with the time offset and milliseconds being optional, e.g.
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
                - the value 0 indicates the current time
                
            date_to (Optional[str]):
                The value has multiple formats similiar to the dateFrom parameter
                - Filters items ending before a date.
        
        Returns:
            Tuple[int, int]:
                Position 1: Successfull Orders, Position 2: Failed orders
                
        Raises:
            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return get_orders_overview_action(
            context=self._ctx,
            controller_id=controller_id,
            date_from=date_from,
            date_to=date_to
        )
        
    def get_order_log(
        self,
        controller_id: str,
        history_id: int
    ) -> Dict[str, Any]:
        """
        Returns the log of an executed order.
        
        Args:
            controller_id (str):
                The ID of the controller from which the order log should be retrieved.
            
            history_id (int):
                The history id of an order.
                
        Returns:
            Dict[str, Any]:
                Array of logEvents.
                
        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return get_order_log_action(
            context=self._ctx,
            controller_id=controller_id,
            history_id=history_id
        )