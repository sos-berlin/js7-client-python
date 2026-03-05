from functools import cached_property

from ...context import Context
from .manage import Manage
from .deploy import Deploy
        

class Inventory:
    def __init__(self, context: Context):
        self._ctx = context
    
    @cached_property
    def manage(self) -> Manage:
        return Manage(context=self._ctx)
    
    @cached_property
    def deploy(self) -> Deploy:
        return Deploy(context=self._ctx)
