from typing import Optional
from pydantic import BaseModel


class GitCredentials(BaseModel):
    email: Optional[str] = None
    git_account: Optional[str] = None
    git_server: Optional[str] = None
    keyfile_path: Optional[str] = None
    password: Optional[str] = None
    personal_access_token: Optional[str] = None
    username: Optional[str] = None