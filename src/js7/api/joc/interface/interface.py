from typing import Optional
from .dispatcher import Dispatcher


class Interface(Dispatcher):
    def __init__(self, version: Optional[str]):
        super().__init__(version=version)
        