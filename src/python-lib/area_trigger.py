from enum import Enum
from material import Material
from shape import Shape

class AreaCondition(str, Enum):
    """Condition an AreaTrigger evaluates against a fixed area of a conveyor."""

    # The commanded WP is fully inside the area. Note this is `contains` and not
    # `intersects`: a pick may only start once the WP is completely within the
    # target area, otherwise the gripper would reach for a WP still rolling in.
    WP_INSIDE = "WP_INSIDE"

    # No WP on the belt touches the area. Used when the commanded WP is off-belt
    # (held by the arm) and needs a free slot to be put down into.
    AREA_CLEAR = "AREA_CLEAR"

    # The commanded WP has been inside the area and has now left it. Used to act
    # on a WP having physically cleared something, which a fixed delay cannot
    # express once the belt may stop part-way through.
    WP_PASSED = "WP_PASSED"

class AreaTrigger:
    """Fires when a workpiece's relation to a fixed area of the conveyor
    satisfies a condition while a specific command is active.

    Detection is rising-edge, keyed by (wp id, triggering command), mirroring
    PositionSensor.is_detected: the trigger reports True on the first tick the
    condition holds and stays silent until the condition has cleared again.
    """

    def __init__(self, name: str, area: Shape, triggering_cmd, target_action: str, condition: AreaCondition, delay: int = 0) -> None:
        self.name = name
        self.area = area
        self.triggering_cmd = triggering_cmd
        self.target_action = target_action
        self.condition = condition
        self.delay = delay
        self._fired = set()
        self._entered = set()

    def _holds(self, wp: Material, wps: list) -> bool:
        if self.condition == AreaCondition.WP_INSIDE:
            return wp in wps and self.area.contains(wp.shape)

        if self.condition == AreaCondition.AREA_CLEAR:
            return not any(self.area.intersects(other.shape) for other in wps)

        assert self.condition == AreaCondition.WP_PASSED, f"Unknown area condition {self.condition}"
        if self.area.intersects(wp.shape):
            self._entered.add(wp.id)
            return False
        # Only counts as passed if the WP was seen inside the area first, so a
        # WP that has not reached it yet does not look like one that is through.
        return wp.id in self._entered

    def is_triggered(self, wp: Material, wps: list) -> bool:
        """Evaluates the condition for `wp` against the workpieces `wps`
        currently on the belt, returning True only on the rising edge.

        Args:
            wp (Material): The workpiece the active command refers to.
            wps (list): The workpieces currently on the conveyor.
        """
        key = (wp.id, self.triggering_cmd)
        holds = self._holds(wp, wps)

        if not holds:
            self._fired.discard(key)
            return False

        if key in self._fired:
            return False

        self._fired.add(key)
        return True

    def __str__(self) -> str:
        return f'AreaTrigger({self.name}, {self.condition.value}, {self.triggering_cmd})'
