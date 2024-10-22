import pymunk
from pymunk import Vec2d


def _get_rectangular_shape_vertices(width: float, height: float, size_multiplier: float, center_position: Vec2d) -> list[Vec2d]:
    x = width / 2.0
    y = height / 2.0
    return [
        center_position + Vec2d(-x, -y) * size_multiplier,
        center_position + Vec2d(x, -y) * size_multiplier,
        center_position + Vec2d(x, y) * size_multiplier,
        center_position + Vec2d(-x, y) * size_multiplier,
    ]

class RectangularBlock:
    def __init__(self, width: float, height: float, center_position: Vec2d, mass: float, rotate_radians: float=0) -> None:
        self._main_body = pymunk.Body()
        self._main_body.position = center_position
        rotation = pymunk.Transform.rotation(rotate_radians)
        self._main_body_shape = pymunk.Poly(
            self._main_body,
            _get_rectangular_shape_vertices(width, height, 2, Vec2d(0,0)),
            rotation
            )
        self._main_body_shape.mass = mass
        self._main_body_shape.friction = 0.7
        
    
    def add_to_space(self, space: pymunk.Space):
        space.add(self._main_body, self._main_body_shape)