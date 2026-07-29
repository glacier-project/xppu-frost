from enum import Enum
from dataclasses import dataclass

class PACmdType(str, Enum):
    MOVE_TO_POS = "MOVE_TO_POS"
    PICKUP_FROM_POS = "PICKUP_FROM_POS"
    PUTDOWN_TO_POS = "PUTDOWN_TO_POS"

class PAPos(str, Enum):
    POS1 = "POS1"
    POS2 = "POS2"
    POS3 = "POS3"
    POS4 = "POS4"

@dataclass(frozen=True, order=True)
class PACmd:
    cmd_type: PACmdType
    position: PAPos
