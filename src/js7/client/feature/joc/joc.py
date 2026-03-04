from functools import cached_property

from ....client.context import Context
from .manage import Manage
from .operate import Operate


class JOC:
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def manage(self) -> Manage:
        return Manage(context=self._ctx)
    
    @cached_property
    def operate(self) -> Operate:
        return Operate(context=self._ctx)