"""
Day 17 - Trick Shot

The probe has a position (x,y) and starts at (0,0)
The probe has an initial velocity in x and y directions

At each step:
- The x position is increased by the x velocity
- The y position is increased by the y velocity
- The x velocity changes by 1 towards 0 and stays at 0 if it is 0
- The y velocity decreases by 1

There is a target area for the probe
For example:
target area: x=20..30, y=-10..-5

At some future step the probe must be within the target area
It is not enough for the probe to 'pass through' the target area and not have a step that is within the target area

Part I
Find the initial velocity that causes the probe to reach the highest y position
 and still eventually be within the target area after any step
What is the highest y position it reaches on this trajectory?

In the example above (6,9) is the best initial velocity reaching a height of 45

My puzzle input is actually:
target area: x=253..280, y=-73..-46
"""

from math import sqrt

class Probe():
    """A class to model a probe"""
    def __init__(self,initial_velocity,target_area):
        """Create the probe
        Its position starts at (0,0)
        Its velocity is set to the initial velocity,
         making sure the x and y components are integers
        """
        self.x_position = 0
        self.y_position = 0
        self.x_velocity = int(initial_velocity[0])
        self.y_velocity = int(initial_velocity[1])
        self.X_MIN = int(target_area[0])
        self.X_MAX = int(target_area[1])
        self.Y_MIN = int(target_area[2])
        self.Y_MAX = int(target_area[3])
        self.max_y_position = 0

    def update_max_y_position(self):
        if self.y_position > self.max_y_position:
            self.max_y_position = self.y_position

    def update_probe_position(self):
        """A method to update the probe's position by one step"""
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        if self.x_velocity > 0:
            self.x_velocity -= 1
        self.y_velocity -= 1
        self.update_max_y_position()

    def check_target_area(self):
        """Check if the probe is in the target area"""
        if self.X_MIN <= self.x_position <= self.X_MAX and self.Y_MIN <= self.y_position <= self.Y_MAX:
            return True

    def fire_probe(self):
        """Fire the probe and see if it hits the target"""
        while self.x_position <= self.X_MAX:     # I the probe yet to reach the target area
            # print(f"X {self.x_position} Y {self.y_position}")
            if self.check_target_area():
                return self.max_y_position
            elif self.y_position <= self.Y_MIN:  # Has the probe overshot the target area
                return "Miss"
            self.update_probe_position()
        return "Miss"                            # If the probe is past the X_MAX and it's not hit the target

def triangular_number(n):
    return n*(n+1)//2

def quadratic_answer(a,b,c):
    min_ans = (-b - sqrt(b**2 - 4*a*c))/(2 * a)
    max_ans = (-b + sqrt(b**2 - 4*a*c))/(2 * a)
    return [min_ans,max_ans]

def main():
    """
    The main program

    Part I
    The height of the probe depends on the initial velocity in the y direction
    The height is n(n+1)/2 where n is the initial velociry in the y direction
    Assuming the target area is below the x axis then the largest initial velocity in the y direction
    is dictated by the largest (most negative) y value of the target area (Y).
    The largest initial velocity n =  Y - 1
    
    Part II
    Need to consider the range of the x and y velocities that still hit the target area.
    Minimum X velocity is x(x+1)/2 = Target Area min X coordinate (or we can start from 0)
    Maximum X velocity is x = Target Area max X coordinate       ######         But I had to add one to get this to work?
    Minimum Y velocity is y = Target Area min Y coordinate
    Maximum Y velocity is y + 1 = abs(Target Area min Y coordinate) as given by part I
    """
    
    test_target_area = [20,30,-10,-5]
    test_velocity_01 = [7,2]    # Max height 3
    test_velocity_02 = [6,3]    # Max height 6
    test_velocity_03 = [9,0]    # Max height 0
    test_velocity_04 = [17,-4]  # Fails to hit target
    test_velocity_05 = [6,9]    # Max height 45
    test_velocity_06 = [6,10]   # Fails to hit target

    TARGET_AREA_X_MIN = 20
    TARGET_AREA_X_MAX = 30
    TARGET_AREA_Y_MIN = -10
    TARGET_AREA_Y_MAX = -5

    TARGET_AREA_X_MIN = 253
    TARGET_AREA_X_MAX = 280
    TARGET_AREA_Y_MIN = -73
    TARGET_AREA_Y_MAX = -46
    my_target_area = [TARGET_AREA_X_MIN,TARGET_AREA_X_MAX,TARGET_AREA_Y_MIN,TARGET_AREA_Y_MAX]

    print(f"Part I - Highest Height is {triangular_number(-my_target_area[2]-1)}")

    MIN_X_VELOCITY = int(quadratic_answer(1,1,-2*TARGET_AREA_X_MIN)[1])
    MIN_X_VELOCITY = 0
    MAX_X_VELOCITY = TARGET_AREA_X_MAX+1
    MIN_Y_VELOCITY = TARGET_AREA_Y_MIN
    MAX_Y_VELOCITY = -TARGET_AREA_Y_MIN

    successful_velocities = []
    for x_velocity in range(MIN_X_VELOCITY,MAX_X_VELOCITY):
        for y_velocity in range(MIN_Y_VELOCITY,MAX_Y_VELOCITY):
            initial_probe_velocity = [x_velocity,y_velocity]
            temp_probe = Probe(initial_probe_velocity,my_target_area)
            result = temp_probe.fire_probe()
            if result != "Miss":
                successful_velocities.append(initial_probe_velocity)
    
    print(f"Part II - Number of successful starting velocities is {len(successful_velocities)}")

if __name__ == "__main__":
    main()
