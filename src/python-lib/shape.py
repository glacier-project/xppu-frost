from abc import abstractmethod
from typing import TypeVar, Tuple, Union
from shapely import Polygon, Point, box
from shapely.affinity import rotate, translate
from shapely.geometry.base import BaseGeometry
from shapely.predicates import crosses, contains, intersects
from f_compare import definitely_greater_than, cos, sin
import numpy as np

class Shape:

    def __init__(self, centroid_pos : Point, angle: float) -> None:
        self.centroid_pos = centroid_pos
        self.poly = None
        self.angle = angle

    # def intersect(self, shape: ShapeType) -> bool:
    #     polygon = self.get_poly()
    #     return polygon.intersects(shape.get_poly())

    def get_poly(self) -> BaseGeometry:
        if self.poly is not None:
            return self.poly
        self.poly = self._get_poly()
        return self.poly

    def translate(self, dx:float=0, dy:float=0, dz:float=0) -> "Shape":
        poly = self.get_poly()
        poly = translate(geom=poly, xoff=dx, yoff=dy, zoff=dz)
        self.poly = poly
        self.centroid_pos = poly.centroid
        return self

    def translate_to(self, x:float=0, y:float=0) -> "Shape":
        self.translate(
            dx=x-self.centroid_pos.x,
            dy=y-self.centroid_pos.y
        )
        return self

    def rotate(self, angle: float, origin : Union[str, Point]= 'center', use_radians: bool = True) -> "Shape":
        poly = self.get_poly()
        poly = rotate(geom=poly, angle=angle, origin=origin, use_radians=use_radians)
        # update angle
        self.angle += angle if use_radians else np.deg2rad(angle)
        self.poly = poly
        self.centroid_pos = poly.centroid
        return self

    def contains(self, shape:"Shape") -> bool:
        return contains(self.get_poly(), shape.get_poly())

    def crosses(self, shape:"Shape") -> bool:
        return crosses(self.get_poly(), shape.get_poly())

    def intersects(self, shape:"Shape") -> bool:
        return intersects(self.get_poly(), shape.get_poly())

    def collision(self, shape:"Shape", direction_angle:float) -> None:

        # get min distance
        d1 = self._get_min_distance()
        d2 = shape._get_min_distance()
        # print(f"{d1=}, {d2=}")

        # get x,y components
        dx = (d1+d2) * cos(direction_angle, 1e-5)
        dy = (d1+d2) * sin(direction_angle, 1e-5)
        # print(f"{dx=}, {dy=}")

        # get coordinates
        shape_position = shape.centroid_pos
        x = shape_position.x - dx
        y = shape_position.y - dy
        # print(f"{shape_position=} {x=}, {y=}")

        # fix position
        self.translate_to(x=x, y=y)

    @abstractmethod
    def _get_min_distance(self) -> float:
        pass

    @abstractmethod
    def _get_poly(self) -> BaseGeometry:
        pass

    @abstractmethod
    def _get_origin(self) -> Point:
        pass

class CircleShape(Shape):
    def __init__(self, centroid_pos : Point, radius: float) -> None:
        super().__init__(centroid_pos, 0)
        self.radius = radius

    def _get_poly(self) -> BaseGeometry:
        return self.centroid_pos.buffer(self.radius)

    def _get_origin(self) -> Point:
        return Point(self.centroid_pos.x-self.radius, self.centroid_pos.y-self.radius)

    def _get_min_distance(self) -> float:
        return self.radius

class RectangularShape(Shape):
    def __init__(self, centroid_pos : Point, base: float, height: float, angle: float) -> None:
        super().__init__(centroid_pos, angle)
        self.base = base
        self.height = height

    def _get_raw_bounds(self) -> Tuple[float, float, float, float]:
        min_x = self.centroid_pos.x - self.base/2
        max_x = self.centroid_pos.x + self.base/2
        min_y = self.centroid_pos.y - self.height/2
        max_y = self.centroid_pos.y + self.height/2
        return min_x, min_y, max_x, max_y

    def _get_poly(self) -> BaseGeometry:
        min_x, min_y, max_x, max_y = self._get_raw_bounds()
        # print(f"{min_x=}, {min_y=}, {max_x=}, {max_y=}")
        # print(f"{self.centroid_pos=}, {self.base=}, {self.height=}")
        poly = Polygon([(max_x, min_y),(max_x, max_y),(min_x, max_y),(min_x, min_y)])
        return rotate(poly, self.angle, origin=self._get_origin(), use_radians=True)

    def _get_origin(self) -> Point:
        min_x, min_y, max_x, max_y = self._get_raw_bounds()
        return Point(min_x, min_y,0)

    def _get_min_distance(self) -> float:
        angle = np.rad2deg(self.angle)
        # 0 - 45
        # 90 - 135
        # 180 - 225
        # 270 - 315
        if (angle // 45) % 2 == 0:
            return (self.base/2)/np.cos(angle%45)
        # 45 - 90
        # 135 - 180
        # 225 - 270
        # 315 - 360
        return (self.height/2)/np.cos(45 - (angle%45))

class MaterialSquareShape(RectangularShape):
    def __init__(self, centroid_pos : Point, base: float, angle: float) -> None:
        super().__init__(centroid_pos, base, base, angle)

class ComponentShape(RectangularShape):
    def __init__(self, centroid_pos : Point, base: float, height: float, angle: float) -> None:
        super().__init__(centroid_pos, base=base, height=height, angle=angle)

    def get_sensor_shape(self, offset:float, width:float, length: float):
        min_x, min_y, max_x, max_y = self._get_raw_bounds()

        # create shape and apply rotation angle
        x = min_x + offset
        return RectangularShape(Point(x+width/2, min_y+length/2), base=width, height=length, angle=0) \
                .rotate(self.angle, origin=self._get_origin(), use_radians=True)

class ConveyorBeltShape(ComponentShape):
    def __init__(self, centroid_pos : Point, base: float, height: float, angle: float) -> None:
        super().__init__(centroid_pos, base=base, height=height, angle=angle)

    def set_init_coordinates(self, shape:Shape, in_direction:str='entry') -> None:
        min_x, min_y, max_x, max_y = shape.get_poly().bounds
        shape_h = np.abs(max_y-min_y)
        shape_b = np.abs(max_x-min_x)

        min_x, min_y, max_x, max_y = self._get_raw_bounds()

        y_offset = (self.height)/2
        assert(definitely_greater_than(self.height,shape_h))
        x_offset = shape_b/2
        assert(definitely_greater_than(x_offset, 0))

        # center shape entry
        if in_direction == 'entry':
            point = Point(min_x+x_offset,min_y+y_offset,0)
        if in_direction == 'exit':
            point = Point(max_x-x_offset,min_y+y_offset,0)

        # rotate to match real conveyor angle
        point = rotate(point, self.angle, origin=self._get_origin(), use_radians=True)

        # translate to the computed point
        shape.translate(
            dx=point.centroid.x-shape.centroid_pos.x,
            dy=point.centroid.y-shape.centroid_pos.y
        )
