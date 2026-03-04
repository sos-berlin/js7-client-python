from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .....model.public.client.common.audit_log import AuditLog


class Account(BaseModel):
    account_name: str
    password: Optional[str] = None
    disabled: Optional[bool] = None
    force_password_change: Optional[bool] = None
    roles: Optional[List[str]] = None
    identity_service_name: str


class BlockedAccount(BaseModel):
    account_name: str
    comment: Optional[str] = None
    blocked_since: Optional[datetime] = None
    audit_log: Optional[AuditLog] = None