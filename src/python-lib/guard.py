from material import Material
from shape import Shape
from shapely import Point

class Guard:

    def __init__(self, name: str, guard_area:Shape, active: bool= False) -> None:
        self.name = name
        self.guard_area = guard_area
        self._allowed_wp = {}
        self._active = active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
        self._allowed_wp.clear()

    def allow_wp(self, wp: Material):
        self._allowed_wp[wp] = wp

    def disallow_wp(self, wp: Material):
        if wp in self._allowed_wp:
            del self._allowed_wp[wp]

    def is_active(self, wp: Material):
        if not self._active:
            return False

        wp_shape = wp.shape
        if not wp_shape.intersects(self.guard_area):
            return False

        return not wp in self._allowed_wp

    def __str__(self) -> str:
        return f'Guard({self.name}, {self.guard_area})'
