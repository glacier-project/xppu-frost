from material import Material
from shape import Shape
from shapely import Point

class PositionSensor:

    def __init__(self, name: str, working_area:Shape) -> None:
        self.name = name
        self.working_area = working_area
        self._last_wps = []

    def is_detected(self, wp: Material) -> bool:
        last_wps = self._last_wps
        detected = self.working_area.intersects(wp.shape)

        # raise evt only the first time
        first_time = wp not in last_wps
        if not detected:
            if wp in last_wps:
                last_wps.remove(wp)

        elif first_time:
            last_wps.append(wp)
            if len(last_wps) > 2:
                last_wps.pop(0)

        return detected and first_time

    def __str__(self) -> str:
        return f'PositionSensor({self.name})'
