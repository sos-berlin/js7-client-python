from pydantic import BaseModel


class Folder(BaseModel):
    folder_path: str
    recursive: bool = True