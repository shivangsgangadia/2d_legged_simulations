import pymunk
import pygame


class PlanarGround:
    COLLISION_CATEGORY = 0b10000
    _instance = None
    _screen = None
    _space = None
    _world_size = (0, 0)
    
    def __init__(self, y_pos: int) -> None:
        self.y_position = y_pos
        self.ground = pymunk.Segment(
            PlanarGround._space.static_body,
            (- 10 * PlanarGround._screen.get_width(), y_pos),
            (10 * PlanarGround._screen.get_width(), y_pos),
            0.0
        )
        
        self.ground.elasticity = 0.95
        self.ground.friction = 0.9
        
        self.ground.filter = pymunk.ShapeFilter(
            categories=PlanarGround.COLLISION_CATEGORY,
        )
    
    def draw_distance_markers(self):
        for i in range(int(PlanarGround._world_size[0] * 3)):
            start_x = (i * 10)
            start_y = self.y_position
            end_x = start_x
            end_y = start_y + 50
            pygame.draw.line(PlanarGround._screen, (200, 0, 0), (start_x, start_y), (end_x, end_y), width=1)
    
    def add_to_space(self):
        PlanarGround._space.add(self.ground)
        
    @classmethod
    def initialize_ground(cls, screen: pygame.Surface, y_pos: int, space: pymunk.Space):
        if cls._instance is None:
            cls._screen = screen
            cls._space = space
            cls._world_size = (cls._screen.get_width(), cls._screen.get_height())
            cls._instance = cls(y_pos)
    
    @classmethod
    def get_ground(cls):
        return cls._instance