from enum import Enum

class StackCmd(str, Enum):
    REQ_WP = "REQ_WP",
    WP_PICKED_UP="WP_PICKED_UP"
