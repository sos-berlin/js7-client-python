from typing import List, Literal, Optional, Set
from pydantic import BaseModel

from ..enum.object_types import ObjectType


ChangeStatus = Literal["DEPLOYED", "VALID", "RELEASED"]


class Change(BaseModel):
    path: Optional[str]
    name: Optional[str] = None
    object_type: ObjectType
    status: Optional[Set[ChangeStatus]] = None


class ChangeDependencies(Change):
    dependencies: List[Change]
