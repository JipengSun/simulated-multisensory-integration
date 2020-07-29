from math import *
import random
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pandas as pd
import time
import sys

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


def policy_update(action_choice,current_error, previous_error, action_policy):
    delta_error = current_error - previous_error
    action_policy[action_choice] -= delta_error
    return action_policy


def action_generator(action_index,policy,action_list,shoulder_angle,elbow_angle):
    is_safe = False
    ban = []
    prob_p = np.zeros(4)
    for i in range(len(prob_p)):
        prob_p[i] = exp(policy[i])
    prob_p /= sum(prob_p)
    while not is_safe:
        temp = np.random.choice(action_index,size=1,p=prob_p)
        while temp[0] in ban:
            temp = np.random.choice(action_index,size=1,p=prob_p)
        d_shoulder,d_elbow = action_list[temp[0]]
        if min_shoulder <= (shoulder_angle + d_shoulder) <= max_shoulder and min_elbow <= (elbow_angle + d_elbow) <= max_elbow:
            is_safe = True
            print(policy)
            print(shoulder_angle,elbow_angle)
        else:
            ban.append(temp[0])
    return temp[0]


def target_reaching(target_x, target_y, max_iteration = 500, reaching_threshhold = 0.5, step_angle = 3):
    # Data recording
    elbow_x_list = []
    elbow_y_list = []
    hand_x_list = []
    hand_y_list = []
    elbow_angle_list = []
    shoulder_angle_list = []
    shoulder_angle = random.uniform(min_shoulder, max_shoulder)
    shoulder_angle_list.append(shoulder_angle)
    elbow_angle = random.uniform(min_elbow, max_elbow)
    elbow_angle_list.append(elbow_angle)
    target_position = (target_x, line_y)
    hand_position = arm_position(shoulder_angle, elbow_angle)
    action_list = [(step_angle, 0), (-step_angle, 0), (0, step_angle), (0, -step_angle)]
    action_index = list(range(0, len(action_list)))
    policy = np.array([1 for i in range(len(action_list))], dtype=np.float)
    current_error = positions_distance(hand_position, target_position)
    elbow_x = upper_length * cos(radians(shoulder_angle))
    elbow_y = upper_length * sin(radians(shoulder_angle))
    elbow_x_list.append(elbow_x)
    elbow_y_list.append(elbow_y)
    hand_x, hand_y = hand_position
    hand_x_list.append(hand_x)
    hand_y_list.append(hand_y)
    n = 0
    while n < max_iteration and current_error > reaching_threshhold:
        print(current_error)
        previous_error = positions_distance(hand_position, target_position)
        action_choice = action_generator(action_index, policy, action_list, shoulder_angle, elbow_angle)
        d_shoulder, d_elbow = action_list[action_choice]
        shoulder_angle += d_shoulder
        shoulder_angle_list.append(shoulder_angle)
        elbow_angle += d_elbow
        elbow_angle_list.append(elbow_angle)
        hand_position = arm_position(shoulder_angle, elbow_angle)
        elbow_x = upper_length * cos(radians(shoulder_angle))
        elbow_y = upper_length * sin(radians(shoulder_angle))
        elbow_x_list.append(elbow_x)
        elbow_y_list.append(elbow_y)
        hand_x, hand_y = hand_position
        hand_x_list.append(hand_x)
        hand_y_list.append(hand_y)
        current_error = positions_distance(hand_position, target_position)
        policy = policy_update(action_choice, current_error, previous_error, policy)
        n += 1
    print(policy)
    return elbow_x_list, elbow_y_list, hand_x_list, hand_y_list, shoulder_angle_list, elbow_angle_list


def arm_animation(target_x, target_y, elbow_x_list, elbow_y_list, hand_x_list, hand_y_list):
    fig = plt.figure()
    ax = plt.axes(xlim=(-6, 6), ylim=(-6, 6))
    line, = ax.plot([], [], color='r')
    line2, = ax.plot([], [], color='yellow')
    line3, = ax.plot([], [], color='b')
    plt.scatter(target_x, target_y, color='g')
    it_text = ax.text(4, 5, '', fontsize=10)

    def init():
        line1x = [0, elbow_x_list[0], hand_x_list[0]]
        line1y = [0, elbow_y_list[0], hand_y_list[0]]
        print(1)
        line.set_data(line1x, line1y)
        line2.set_data(elbow_x_list[0], elbow_y_list[0])
        line2.set_marker('o')
        line3.set_data(hand_x_list[0], hand_y_list[0])
        line3.set_marker('o')
        it_text.set_text('Iteration: %d' % (0))
        # m = int(sys.stdin.readline())
        return line, line2, line3, it_text,

    def animate(i):
        line1x = [0, elbow_x_list[i], hand_x_list[i]]
        line1y = [0, elbow_y_list[i], hand_y_list[i]]
        line.set_data(line1x, line1y)
        line2.set_data(elbow_x_list[i], elbow_y_list[i])
        line2.set_marker('o')
        line3.set_data(hand_x_list[i], hand_y_list[i])
        line3.set_marker('o')
        it_text.set_text('Iteration: %d' % (i))
        return line, line2, line3, it_text,

    ani = anim.FuncAnimation(fig, animate, range(len(elbow_x_list)), init_func=init, interval=200, repeat=False)
    # ani.save('2-dof-arm.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    f = r"/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/2-dof_video.mp4"
    writervideo = anim.FFMpegWriter(fps=60)
    ani.save(f, writer=writervideo)
    plt.show()


if __name__ == '__main__':
    # Randomly generate target position
    line_y = 3
    left_x, right_x, = valid_position_range(line_y)
    target_x = random.uniform(left_x, right_x)
    elbow_x_list, elbow_y_list, hand_x_list, hand_y_list, shoulder_angle_list, elbow_angle_list \
        = target_reaching(target_x, line_y, max_iteration = 500, reaching_threshhold = 0.5, step_angle = 3)
    arm_animation(target_x,line_y,elbow_x_list, elbow_y_list, hand_x_list, hand_y_list)
    dataframe = pd.DataFrame({'elbow_x':elbow_x_list,'elbow_y':elbow_y_list,'hand_x':hand_x_list,'hand_y':hand_y_list,'shoulder_angle':shoulder_angle_list,'elbow_angle':elbow_angle_list})
    dataframe.to_csv(r"/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/simulated_data.csv")




