from typing import Optional
from pydantic import BaseModel


class AuditLog(BaseModel):
    ticket_link: Optional[str] = None
    comment:     Optional[str] = None
    time_spent:  Optional[int] = None