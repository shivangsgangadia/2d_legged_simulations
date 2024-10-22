import pymunk


class ControlledMotor(pymunk.SimpleMotor):
    def __init__(self, a: pymunk.Body, b: pymunk.Body) -> None:
        super().__init__(a, b, 0.0)
        self.max_force = 10000000
        self.target_angle = 0
        self.post_solve = self.move_towards_target_position
        
    def set_speed(self, speed: float):
        self.rate = speed
    
    def get_current_angle(self) -> float:
        angle = self.a.rotation_vector.get_angle_degrees_between(self.b.rotation_vector)
        if angle < 0:
            angle = - angle
        elif 180 > angle > 0:
            angle = 360 - angle
        return angle
    
    def set_target_angle_degrees(self, angle: float):
        self.target_angle = angle
    
    def move_towards_target_position(self, constraint, space: pymunk.Space):
        angle_diff =  self.target_angle - self.get_current_angle()
        # Deal with the 0-360 limitation
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        elif angle_diff < -180:
            angle_diff = 360 + angle_diff
        
        p_term = (0.5 * angle_diff)
        d_term = (0.00005 * (angle_diff / 0.01))
        # print(f"P: {p_term}\tD: {d_term}")
        self.rate = p_term - d_term