from pydantic import BaseModel


class ClientConfiguration(BaseModel):
    timezone: str = "Etc/UTC"
    """see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""
