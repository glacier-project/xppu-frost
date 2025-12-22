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
        key = (wp.id, triggering_cmd)
        last_wps = self._last_wps
        detected = self.working_area.intersects(wp.shape)

        # raise evt only the first time
        # logger.warning(f'PositionSensor {self.name} checking detection for WP {wp.id} for command {triggering_cmd}: detected={detected} working_area={self.working_area.centroid_pos} wp_shape={wp.shape.centroid_pos}')
        first_time = key not in last_wps
        if not detected and key in last_wps:
            # logger.error(f'PositionSensor {self.name} no longer detects {detected} WP {wp.id} for command {triggering_cmd} working_area={self.working_area.get_poly()} wp_shape={wp.shape.centroid_pos}')
            last_wps.remove(key)
        elif detected and first_time:
            # logger.error(f'PositionSensor {self.name} detected WP {wp.id} for command {triggering_cmd} working_area={self.working_area.get_poly()} wp_shape={wp.shape.centroid_pos}')
            last_wps.add(key)
            return True

        return False

    def __str__(self) -> str:
        return f'PositionSensor({self.name})'
