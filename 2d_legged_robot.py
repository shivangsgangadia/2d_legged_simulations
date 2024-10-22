from BaseBodies.Quadruped2D import Quadruped2D
from SimulationEnvironment import SimulationEnvironment

def main():
    # Initial setup of environment and object
    environment = SimulationEnvironment()
    quadruped = Quadruped2D(
        screen_center=environment.screen_center + (0, 200),
        ground_collision_category=environment.collision_category
    )
    # New bots must implement this method
    quadruped.add_bot_to_space(environment.space)
    
    # This pattern is dynamically used to update quadruped values
    quadruped.front_limbs[0].upper_motor.set_target_angle_degrees(60)
    quadruped.front_limbs[0].lower_motor.set_target_angle_degrees(-60)
    quadruped.front_limbs[1].upper_motor.set_target_angle_degrees(30)
    quadruped.front_limbs[1].lower_motor.set_target_angle_degrees(-60)
    
    quadruped.back_limbs[0].upper_motor.set_target_angle_degrees(60)
    quadruped.back_limbs[0].lower_motor.set_target_angle_degrees(-60)
    quadruped.back_limbs[1].upper_motor.set_target_angle_degrees(30)
    quadruped.back_limbs[1].lower_motor.set_target_angle_degrees(-60)
    
    while True:
        environment.step_simulation()

if __name__ == '__main__':
    main()
