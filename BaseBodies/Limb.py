from BaseBodies.RectangularBlock import RectangularBlock
import pymunk
from pymunk import Vec2d
import math
from BaseBodies.ControlledMotor import ControlledMotor

class Limb:
    UPPER_BODY_COLOR = (100, 100, 50, 255)
    LOWER_BODY_COLOR = (50, 100, 100, 255)
    def __init__(self, position: Vec2d, upper_length: float, upper_thickness: float, lower_length: float, lower_thickness: float, mass: float, collision_category: int, collision_mask: int = 0b0) -> None:
        self.upper_body = RectangularBlock(
                                width=upper_length,
                                height=upper_thickness,
                                center_position=position,
                                mass=mass,
                                rotate_radians=math.pi / 2
                            )
        
        self.upper_body._main_body_shape.filter = pymunk.ShapeFilter(
            categories=collision_category,
            mask=collision_mask
        )
        self.upper_body._main_body_shape.color = Limb.UPPER_BODY_COLOR
        
        self.upper_motor: ControlledMotor = None
        self.upper_joint: pymunk.PivotJoint = None
        
        self.lower_body_joint_position = (
            position
            + (0, upper_length * 2 / 3)
        )
        
        self.lower_body_position = (
            self.lower_body_joint_position
            + (0, lower_length * 2 / 3)
        )
        
        self.lower_body = RectangularBlock(
                                width=lower_length,
                                height=lower_thickness,
                                center_position=self.lower_body_position,
                                mass=mass,
                                rotate_radians=math.pi / 2
                            )
        
        self.lower_body._main_body_shape.filter = pymunk.ShapeFilter(
            categories=collision_category,
            mask=collision_mask
        )
        self.lower_body._main_body_shape.color = Limb.LOWER_BODY_COLOR
        
        self.lower_joint = pymunk.PivotJoint(
                                self.upper_body._main_body,
                                self.lower_body._main_body,
                                self.lower_body_joint_position
                            )
        
        self.lower_motor = ControlledMotor(self.upper_body._main_body, self.lower_body._main_body)
    
    def attach_to_body(self, b: pymunk.Body, position: Vec2d):
        self.upper_joint = pymunk.PivotJoint(
                                b,
                                self.upper_body._main_body,
                                position
                            )
        self.upper_motor = ControlledMotor(b, self.upper_body._main_body)
    
    def add_to_space(self, space: pymunk.Space):
        self.upper_body.add_to_space(space)
        self.lower_body.add_to_space(space)
        space.add(
            self.upper_joint,
            self.upper_motor,
            self.lower_joint,
            self.lower_motor
        )