from typing import Optional
from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime
from typing import List, Optional


#---------------#
# Configuration #
#---------------#
def snake_to_camel_case(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


class BaseModel(PydanticBaseModel):
    model_config = {
        "alias_generator": snake_to_camel_case,
        "populate_by_name": True,
        "extra": "ignore",
    }


#------#
# Base #
#------#
class JocErr(BaseModel):
    code: str
    message: str


class Err420(BaseModel):
    delivery_date: datetime
    survey_date: Optional[datetime] = None
    error: JocErr


class Err419(BaseModel):
    survey_date: Optional[datetime] = None
    path: Optional[str] = None
    code: str
    message: str


class Approver(BaseModel):
    account_name: str
    first_name: str
    last_name: str
    email: Optional[str] = None


class FourEyesResponse(BaseModel):
    delivery_date: datetime
    message: str
    approvers: List[Approver]
    requestor: Optional[str] = None
    request_url: Optional[str] = None
    
    
class AuthenticationResponse(BaseModel):
    is_authenticated: bool
    message: Optional[str] = None
    account: Optional[str] = None
    role: Optional[str] = None
    is_permitted: Optional[bool] = None
    session_timeout: Optional[int] = None


#------------#
# Exceptions #
#------------#
class JocError(Exception):
    """Base class for all JOC-related errors."""

    status_code: int
    path: Optional[str]

    def __init__(self, message: str, *, path: Optional[str] = None):
        self.path = path
        super().__init__(message)
    
    
class AuthenticationFailed(JocError):
    status_code = 401

    def __init__(self, response: AuthenticationResponse, *, path: Optional[str] = None):
        self.response = response
        super().__init__(
            response.message or "Authentication failed",
            path=path
        )
        
        
class PermissionDenied(JocError):
    status_code = 403

    def __init__(self, response: AuthenticationResponse, *, path: Optional[str] = None):
        self.response = response
        super().__init__(
            response.message or "Permission denied",
            path=path
        )
        
        
class SessionExpired(JocError):
    status_code = 440

    def __init__(self, response: AuthenticationResponse, *, path: Optional[str] = None):
        self.response = response
        super().__init__(
            response.message or "Session expired",
            path=path
        )


class JocValidationFailed(JocError):
    status_code = 419

    def __init__(self, error: Err419, *, path: Optional[str] = None):
        self.error = error
        self.code = error.code
        self.survey_date = error.survey_date

        super().__init__(
            f"[{self.code}] {error.message}",
            path=path or error.path
        )
        
    
class JocOperationFailed(JocError):
    status_code = 420

    def __init__(self, error: Err420, *, path: Optional[str] = None):
        self.error = error
        self.code = error.error.code
        self.delivery_date = error.delivery_date

        super().__init__(
            f"[{self.code}] {error.error.message}",
            path=path
        )


class ApprovalRequired(JocError):
    status_code = 433

    def __init__(self, response: FourEyesResponse, *, path: Optional[str] = None):
        self.response = response
        super().__init__(
            response.message,
            path=path
        )