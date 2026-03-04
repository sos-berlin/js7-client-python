from datetime import datetime, timezone
from typing import Optional, Union
from pydantic import BaseModel


class ScheduleTime(BaseModel):
    value: str

    @classmethod
    def normalize(cls, value: Optional[Union[str, float, int]]) -> Optional["ScheduleTime"]:
        if value is None:
            return None

        # numeric epoch millis
        if isinstance(value, (int, float)):
            ts = value / 1000.0
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return ScheduleTime.at(dt)

        # numeric string → epoch millis
        if value.replace(".", "", 1).isdigit():
            ts = float(value) / 1000.0
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return ScheduleTime.at(dt)

        # plain JS7 string
        return ScheduleTime(value=value)
    
    @classmethod
    def now(cls) -> "ScheduleTime":
        return cls(value="now")

    @classmethod
    def never(cls) -> "ScheduleTime":
        return cls(value="never")

    @classmethod
    def now_plus_seconds(cls, seconds: int) -> "ScheduleTime":
        return cls(value=f"now + {seconds}")

    @classmethod
    def now_plus_hms(cls, hours: int = 0, minutes: int = 0, seconds: int = 0) -> "ScheduleTime":
        return cls(value=f"now + {hours:02d}:{minutes:02d}:{seconds:02d}")

    @classmethod
    def at(cls, dt: datetime) -> "ScheduleTime":
        return cls(value=dt.strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self) -> str:
        return self.value
