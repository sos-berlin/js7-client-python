from functools import cached_property

from .deploy import Deploy
from .manage import Manage
from .operate import Operate

from ....client.context import Context


class Agent:
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def deploy(self) -> Deploy:
        return Deploy(context=self._ctx)
    
    @cached_property
    def manage(self) -> Manage:
        return Manage(context=self._ctx)
    
    @cached_property
    def operate(self) -> Operate:
        return Operate(context=self._ctx)
    
    