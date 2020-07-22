from math import *
import random

# Variable for basic angles
upper_length = 3
fore_length = 2
shoulder_angle = 3
elbow_angle = 3
min_shoulder = 45
max_shoulder = 135
min_elbow = 45
max_elbow = 180

def angle2muscle(shoulder_angle, elbow_angle):
    shoulder_ext = (shoulder_angle-min_shoulder)/(max_shoulder-min_shoulder)
    shoulder_flex = 1 - shoulder_ext
    elbow_ext = (elbow_angle-min_elbow)/(max_elbow-min_elbow)
    elbow_flex = 1 - elbow_ext
    return (shoulder_ext,shoulder_flex,elbow_ext,elbow_flex)

def elbow_angle_reform(angle):
    pass

def arm_position(shoulder_angle, elbow_angle):
    abs_elbow = 180 + shoulder_angle - elbow_angle
    x_arm = upper_length * cos(radians(shoulder_angle)) + fore_length * cos(radians(abs_elbow))
    y_arm = upper_length * sin(radians(shoulder_angle)) + fore_length * sin(radians(abs_elbow))
    return (x_arm,y_arm)


def positions_distance(arm_position,target_position):
    x_arm,y_arm = arm_position
    x_target,y_target = target_position
    return sqrt((x_arm-x_target)**2 + (y_arm-y_target)**2)

# Get valid target position range on a line
def valid_position_range(line_y):
    # The law of cosines, calculate the limit of the y projection of forearm
    min_y = sqrt(upper_length**2 + fore_length**2 - 2*upper_length*fore_length*cos(radians(min_elbow)))
    max_y = sqrt(upper_length**2 + fore_length**2 - 2*upper_length*fore_length*cos(radians(max_elbow)))
    bias_degree = degrees(acos((upper_length**2+max_y**2-fore_length**2)/(2*upper_length*max_y)))
    # Calculate the limit of the y when the shoulder_angle reach its maximum. When y is shorter than this limit, the shoulder_angle limit will exceed.
    left_min_limit_y = max_y * sin(radians(max_shoulder-bias_degree))
    right_min_limit_y = max_y * sin(radians(min_shoulder-bias_degree))

    if line_y < min_y or line_y > max_y:
        print("Unreachable y.")
        print ('Suggested range: '+ str(min_y) + ' ~ ' + str(max_y))
        return None
    if line_y < left_min_limit_y:
        left_x =  max_y*cos(radians(max_shoulder-bias_degree))
    if left_min_limit_y <= line_y <= max_y:
        left_x = -sqrt(max_y**2 - line_y**2)
    if line_y < right_min_limit_y:
        right_x = max_y*cos(radians(min_shoulder-bias_degree))
    if right_min_limit_y <= line_y <= max_y:
        right_x = sqrt(max_y**2 - line_y**2)
    return (left_x,right_x)

if __name__ == '__main__':
    left_x,right_x, = valid_position_range(3)
    target_position = random.uniform(left_x,right_x)
    print target_position
