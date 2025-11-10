from material import Material
from shape import ComponentShape

def set_wp_coordinates_to(wp: Material, area: ComponentShape) -> None:
    wp.shape.translate_to(area.centroid_pos.x, area.centroid_pos.y)