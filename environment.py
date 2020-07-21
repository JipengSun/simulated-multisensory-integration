from math import *

# Variable for basic angles
upper_length = 3
fore_length = 2
shoulder_angle = 3
elbow_angle = 3
min_shoulder = -45
max_shoulder = 135
min_elbow = 0
max_elbow = 135

def angle2muscle(shoulder_angle, elbow_angle):
    shoulder_ext = (shoulder_angle-min_shoulder)/(max_shoulder-min_shoulder)
    shoulder_flex = 1 - shoulder_ext
    elbow_ext = (elbow_angle-min_elbow)/(max_elbow-min_elbow)
    elbow_flex = 1 - elbow_ext
    return shoulder_ext,shoulder_flex,elbow_ext,elbow_flex

def elbow_angle_reform(angle):
    pass

def arm_position(shoulder_angle, elbow_angle):
    abs_elbow = 180 + shoulder_angle - elbow_angle
    x_arm = upper_length * cos(shoulder_angle) + fore_length * cos(abs_elbow)
    y_arm = upper_length * sin(shoulder_angle) + fore_length * sin(abs_elbow)
    return x_arm,y_arm

