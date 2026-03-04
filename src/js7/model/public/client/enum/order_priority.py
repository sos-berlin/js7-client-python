from enum import Enum


class OrderPriority(int, Enum):
    LOW          = -20000
    BELOW_NORMAL = -10000
    NORMAL       = 0
    ABOVE_NORMAL = 10000
    HIGH         = 20000