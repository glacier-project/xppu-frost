from enum import IntEnum

class MonostableCylinderState(IntEnum):
    RETRACTED = 1
    EXTENDED = 2
    RETRACTING = 3
    EXTENDING = 4

class MonostableCylinderCmd(IntEnum):
    RETRACT = 1
    EXTEND = 2