from datetime import time
from pydantic import BaseModel, field_serializer


class Cycle(BaseModel):
    begin: time
    end: time
    repeat: time

    @field_serializer("begin", "end", "repeat")
    def serialize_time(self, value: time) -> str:
        return value.strftime("%H:%M:%S")