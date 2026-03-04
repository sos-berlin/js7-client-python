from functools import cached_property

from ....client.context import Context

from .manage import Manage

   
class DailyPlan:
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def manage(self) -> Manage:
        return Manage(context=self._ctx)
