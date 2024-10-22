import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from BaseBodies.PlanarGround import PlanarGround

class SimulationEnvironment:
    def __init__(self):
        pygame.init()
        font = pygame.font.Font(None, 24)
        self._screen = pygame.display.set_mode((1000, 1000))
        self.screen_center = Vec2d(
            self._screen.get_width() / 2,
            self._screen.get_height() / 2
        )
        self.clock = pygame.time.Clock()
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)
        self.draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self.terrain_y_position = self._screen.get_height() - 100
        PlanarGround.initialize_ground(self._screen, self.terrain_y_position, self._space)
        PlanarGround.get_ground().add_to_space()

    def step_simulation(self):
        """
        Handles pygame events and pymunk simulation stepping
        Should be iterated in a loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self._screen.fill(pygame.Color("white"))

        self.space.step(0.01)
        PlanarGround.get_ground().draw_distance_markers()

        self.space.debug_draw(self.draw_options)
        pygame.display.flip()

        self.clock.tick(60)

    @property
    def space(self):
        return self._space

    @property
    def collision_category(self):
        return PlanarGround.COLLISION_CATEGORY