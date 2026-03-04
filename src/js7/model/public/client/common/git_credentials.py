from typing import Optional
from pydantic import BaseModel


class GitCredentials(BaseModel):
    email: str
    git_account: str
    git_server: str
    keyfile_path: Optional[str] = None
    password: Optional[str] = None
    personal_access_token: Optional[str] = None
    username: str