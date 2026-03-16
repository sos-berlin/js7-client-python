from typing import Literal, Optional

from pydantic import BaseModel


class Controller(BaseModel):
    url: str
    cluster_url: Optional[str]
    role: Literal["STANDALONE", "PRIMARY", "BACKUP"]
    title: Optional[str]