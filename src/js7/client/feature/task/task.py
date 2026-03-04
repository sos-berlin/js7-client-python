from functools import cached_property
from typing import Any, Dict

from ....client.context import Context
from ....model.public.client.filter.tasks_filter import TasksFilter

from ...action.task.get_task_history_info_action import get_task_history_info_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context

    def get_task_history_info(
        self,
        controller_id: str,
        filter: TasksFilter
    ) -> Dict[str, Any]:
        """
        Args:
            controller_id (str): 
                Identifier of the controller on which the search is executed.
            
            filter (TasksFilter): 
                Filter used to control the results.

        Returns:
            Dict ([str, Any]): 
                A JSON representation of the task history.
            
        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return get_task_history_info_action(
            context=self._ctx,
            controller_id=controller_id,
            filter=filter            
        )


class Task:
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def manage(self) -> Manage:
        return Manage(context=self._ctx)
    