from enum import Enum

class MotorCMD(str, Enum):
    IDLE = 'IDLE'
    CW = 'CW' # clockwise
    CCW = 'CCW' # counterclockwise

class CraneCmd(str, Enum):
    ROTATE_S = "ROTATE_S",
    ROTATE_LSC = "ROTATE_LSC",
    ROTATE_ST = "ROTATE_ST",
    PICKUP_WP = "PICKUP_WP",
    PUTDOWN_WP = "PUTDOWN_WP"

# TODO: Add NONE position
class CranePos(str, Enum):
    POS_S = "POS_S"
    POS_LSC = "POS_LSC"
    POS_ST = "POS_ST"
