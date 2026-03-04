from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.input.add_order import Order
from ....model.public.client.filter.resume_order_filter import ResumeOrderFilter
from ....model.public.client.filter.suspend_order_filter import SuspendOrderFilter

from ...action.order.cancel_orders_action import cancel_orders_action
from ...action.order.continue_orders_action import continue_orders_action
from ...action.order.remove_terminated_orders_action import remove_terminated_orders_action
from ...action.order.resume_orders_action import resume_orders_action
from ...action.order.suspend_orders_action import suspend_orders_action
from ...action.order.confirm_orders_action import confirm_orders_action
from ...action.order.add_orders_action import add_orders_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
        
    def cancel_orders(
        self,
        controller_id: str,
        order_ids: Optional[List[str]] = None,
        workflow_paths: Optional[List[str]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Cancel orders on the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be canceled.

            order_ids (Optional[List[str]]):
                A list of specific order IDs to be canceled.

            workflow_paths (Optional[List[str]]):
                A list of workflow paths whose orders
                should be canceled.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the orders were successfully canceled,
                otherwise `False`.

        Raises:
            ValueError:
                If neither `order_ids` nor `workflow_paths` is provided,
                or if arguments are invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return cancel_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def continue_orders(
        self,
        controller_id: str,
        order_ids: Optional[List[str]] = None,
        workflow_paths: Optional[List[str]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Continue paused or waiting orders on the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be continued.

            order_ids (Optional[List[str]]):
                A list of specific order IDs to be continued.

            workflow_paths (Optional[List[str]]):
                A list of workflow paths whose orders
                should be continued.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the orders were successfully continued,
                otherwise `False`.

        Raises:
            ValueError:
                If neither `order_ids` nor `workflow_paths` is provided,
                or if arguments are invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return continue_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def remove_terminated_orders(
        self,
        controller_id: str,
        order_ids: Optional[List[str]] = None,
        workflow_paths: Optional[List[str]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Remove terminated orders from the specified controller.

        Args:
            controller_id (str):
                The ID of the controller from which terminated
                orders should be removed.

            order_ids (Optional[List[str]]):
                A list of specific terminated order IDs to be removed.

            workflow_paths (Optional[List[str]]):
                A list of workflow paths whose terminated orders
                should be removed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the terminated orders were successfully removed,
                otherwise `False`.

        Raises:
            ValueError:
                If neither `order_ids` nor `workflow_paths` is provided,
                or if arguments are invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return remove_terminated_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def resume_orders(
        self,
        controller_id: str,
        filter: ResumeOrderFilter,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Resume suspended or failed orders on the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be resumed.

            filter (ResumeOrderFilter):
                Defines the criteria used to select the orders
                to be resumed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the orders were successfully resumed,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return resume_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            filter=filter,
            audit_log=audit_log
        )
        
    def suspend_orders(
        self,
        controller_id: str,
        filter: SuspendOrderFilter,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Suspend orders on the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be suspended.

            filter (SuspendOrderFilter):
                Defines the criteria used to select the orders
                to be suspended.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the orders were successfully suspended,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return suspend_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            filter=filter,
            audit_log=audit_log
        )
        
    def confirm_orders(
        self,
        controller_id: str,
        order_ids: Optional[List[str]] = None,
        workflow_paths: Optional[List[str]] = None,
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Confirm prompting orders on the specified controller.

        This operation applies to workflows that include a
        "Prompt" block and require manual confirmation.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be confirmed.

            order_ids (Optional[List[str]]):
                A list of specific order IDs to be confirmed.

            workflow_paths (Optional[List[str]]):
                A list of workflow paths for which prompting
                orders should be confirmed.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            bool:
                Returns `True` if the confirmation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If neither `order_ids` nor `workflow_paths` is provided,
                or if arguments are invalid.

            RuntimeError:
                If the operation fails or the server version
                is incompatible.
        """
        
        return confirm_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            order_ids=order_ids,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def add_orders(
        self,
        controller_id: str,
        orders: List[Order],
        audit_log: Optional[AuditLog] = None
    ) -> List[str]:
        """
        Create new orders on the specified controller.

        Args:
            controller_id (str):
                The ID of the controller on which the orders
                should be created.

            orders (List[Order]):
                A list of order objects to be created.

            audit_log (Optional[AuditLog]):
                Optional audit log information to create an audit entry
                for this operation.

        Returns:
            List[str]:
                A list of the created order IDs.

        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If order creation fails or the server version
                is incompatible.
        """
        
        return add_orders_action(
            context=self._ctx,
            controller_id=controller_id,
            orders=orders,
            audit_log=audit_log
        )