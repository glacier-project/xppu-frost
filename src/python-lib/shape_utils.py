from shape import ComponentShape
from material import Material


def set_wp_coordinates_to(wp: Material, area: ComponentShape) -> None:
    wp.shape.translate_to(area.centroid_pos.x, area.centroid_pos.y)
