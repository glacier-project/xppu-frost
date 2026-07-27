from material import Material
from shape import Shape, SENSOR_COLOR
from shapely import Point
import logging

logger = logging.getLogger(__name__)
class PositionSensor:

    def __init__(self, name: str, working_area:Shape) -> None:
        self.name = name
        working_area.color = SENSOR_COLOR
        self.working_area = working_area
        self._last_wps = set()

    def is_detected(self, wp: Material, triggering_cmd: str) -> bool:
        # A (wp, command) pair is reported as detected only on the rising edge,
        # i.e. the first tick its shape intersects the working area.
        key = (wp.id, triggering_cmd)
        last_wps = self._last_wps
        detected = self.working_area.intersects(wp.shape)

        first_time = key not in last_wps
        if not detected and key in last_wps:
            last_wps.remove(key)
        elif detected and first_time:
            last_wps.add(key)
            return True

        return False

    def __str__(self) -> str:
        return f'PositionSensor({self.name})'
