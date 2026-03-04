from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel, model_validator


class BasicAuth(BaseModel):
    username: str
    password: str


class CertAuth(BaseModel):
    certfile_path: Union[Path, str]
    keyfile_path: Union[Path, str]


class AuthConfiguration(BaseModel):
    basic_auth: Optional[BasicAuth] = None
    cert_auth: Optional[CertAuth]  = None
    
    @model_validator(mode="after")
    def validate_exactly_one_auth(self):
        if (self.basic_auth is None) == (self.cert_auth is None):
            raise ValueError("Exactly one of 'basic_auth' or 'cert_auth' must be provided.")
        return self
