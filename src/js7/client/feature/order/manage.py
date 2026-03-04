from typing import Any, Dict, List

from ...context import Context
from ....model.public.client.filter.order_history_filter import OrderHistoryFilter
from ....model.public.client.filter.get_order_filter import GetOrderFilter
from ....model.public.client.input.add_order import Order

from ...action.order.get_order_history_action import get_order_history_action
from ...action.order.get_orders_action import get_orders_action


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

    