from BaseBodies.RectangularBlock import RectangularBlock
from BaseBodies.ControlledMotor import ControlledMotor
from pymunk import Vec2d
import pymunk
import math
from BaseBodies.Limb import Limb


class Quadruped2D:
    QUADRUPED_MAIN_BODY_WIDTH = 160
    QUADRUPED_MAIN_BODY_HEIGHT = 30
    QUADRUPED_MAIN_BODY_MASS = 40
    QUADRUPED_MAIN_BODY_COLOR = (10, 10, 150, 255)
    
    QUADRUPED_FEMUR_WIDTH = 60
    QUADRUPED_FEMUR_HEIGHT = 10
    QUADRUPED_FEMUR_MASS = 10
    QUADRUPED_FEMUR_COLOR = (100, 100, 50, 255)

    QUADRUPED_KNEE_WIDTH = 60
    QUADRUPED_KNEE_HEIGHT = 10
    QUADRUPED_KNEE_MASS = 10
    QUADRUPED_KNEE_COLOR = (50, 100, 100, 255)

    QUADRUPED_BACK_LIMBS_CATEGORY   = 0b001
    QUADRUPED_FRONT_LIMBS_CATEGORY  = 0b010
    QUADRUPED_TORSO_CATEGORY        = 0b100

    QUADRUPED_BACK_LIMBS_COLLISION_MASK = 0b0
    QUADRUPED_FRONT_LIMBS_COLLISION_MASK = 0b0
    QUADRUPED_TORSO_COLLISION_MASK = 0b0
    
    def __init__(self, screen_center: Vec2d, ground_collision_category: int) -> None:
        self.torso = RectangularBlock(
            width=Quadruped2D.QUADRUPED_MAIN_BODY_WIDTH,
            height=Quadruped2D.QUADRUPED_MAIN_BODY_HEIGHT,
            center_position=screen_center,
            mass=Quadruped2D.QUADRUPED_MAIN_BODY_MASS
        )
        self.torso._main_body_shape.color = Quadruped2D.QUADRUPED_MAIN_BODY_COLOR
        self.torso._main_body_shape.filter = pymunk.ShapeFilter(
            categories=Quadruped2D.QUADRUPED_TORSO_CATEGORY,
            mask=Quadruped2D.QUADRUPED_TORSO_COLLISION_MASK | ground_collision_category
            )
        
        self.back_hip_joint_position = (
            screen_center
            - (Quadruped2D.QUADRUPED_MAIN_BODY_WIDTH / 1.5, 0)
        )
        
        self.back_femur_position = (
            self.back_hip_joint_position
            + (0, Quadruped2D.QUADRUPED_FEMUR_WIDTH * 2 / 3)
            )
        
        self.front_hip_joint_position = (
            screen_center
            + (Quadruped2D.QUADRUPED_MAIN_BODY_WIDTH / 1.5, 0)
        )
        
        self.front_femur_position = (
            self.front_hip_joint_position
            + (0, Quadruped2D.QUADRUPED_FEMUR_WIDTH * 2 / 3)
            )
        
        self.front_limbs = [
            Limb(
                self.front_femur_position,
                Quadruped2D.QUADRUPED_FEMUR_WIDTH,
                Quadruped2D.QUADRUPED_FEMUR_HEIGHT,
                Quadruped2D.QUADRUPED_KNEE_WIDTH,
                Quadruped2D.QUADRUPED_KNEE_HEIGHT,
                Quadruped2D.QUADRUPED_FEMUR_MASS,
                Quadruped2D.QUADRUPED_FRONT_LIMBS_CATEGORY,
                ground_collision_category
            )
            for _ in range(2)
        ]
        
        for limb in self.front_limbs:
            limb.attach_to_body(self.torso._main_body, self.front_hip_joint_position)
        
        self.back_limbs = [
            Limb(
                self.back_femur_position,
                Quadruped2D.QUADRUPED_FEMUR_WIDTH,
                Quadruped2D.QUADRUPED_FEMUR_HEIGHT,
                Quadruped2D.QUADRUPED_KNEE_WIDTH,
                Quadruped2D.QUADRUPED_KNEE_HEIGHT,
                Quadruped2D.QUADRUPED_FEMUR_MASS,
                Quadruped2D.QUADRUPED_FRONT_LIMBS_CATEGORY,
                ground_collision_category
            )
            for _ in range(2)
        ]
        
        for limb in self.back_limbs:
            limb.attach_to_body(self.torso._main_body, self.back_hip_joint_position)
        

    
    def add_bot_to_space(self, space: pymunk.Space):
        self.front_limbs[0].add_to_space(space)
        self.back_limbs[0].add_to_space(space)

        self.torso.add_to_space(space)
        # Debug - keeps robot suspended
        # space.add(pymunk.PivotJoint(self.torso._main_body, space.static_body, self.torso._main_body.position))
        # space.add(pymunk.PivotJoint(self.torso._main_body, space.static_body, self.front_hip_joint_position))
        
        self.front_limbs[1].add_to_space(space)
        self.back_limbs[1].add_to_space(space)
        

        
    
    
        