from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel


class HTTPConfiguration(BaseModel):
    host: str
    port: int
    ssl: bool = False
    cafile_path: Optional[Union[Path, str]] = None
