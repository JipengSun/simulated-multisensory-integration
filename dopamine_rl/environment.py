from math import *
import random
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
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

if __name__ == '__main__':
    n = 0
    line_y = 3
    left_x, right_x, = valid_position_range(line_y)
    target_x = random.uniform(left_x, right_x)
    shoulder_angle = random.uniform(min_shoulder, max_shoulder)
    elbow_angle = random.uniform(min_elbow, max_elbow)
    target_position = (target_x,line_y)
    hand_position = arm_position(shoulder_angle, elbow_angle)
    action_list = [(3,0),(-3,0),(0,3),(0,-3)]
    action_index = list(range(0,len(action_list)))
    policy = np.array([1,1,1,1],dtype=np.float)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    current_error = positions_distance(hand_position, target_position)
    while n < 500 and current_error > 0.5:
        print(current_error)
        elbow_x = upper_length*cos(radians(shoulder_angle))
        elbow_y = upper_length*sin(radians(shoulder_angle))
        x1.append(elbow_x)
        y1.append(elbow_y)
        hand_x, hand_y = hand_position
        x2.append(hand_x)
        y2.append(hand_y)
        previous_error = positions_distance(hand_position,target_position)
        action_choice = action_generator(action_index,policy,action_list,shoulder_angle,elbow_angle)
        d_shoulder,d_elbow = action_list[action_choice]
        shoulder_angle += d_shoulder
        elbow_angle += d_elbow
        hand_position = arm_position(shoulder_angle, elbow_angle)
        current_error = positions_distance(hand_position,target_position)
        policy = policy_update(action_choice,current_error,previous_error,policy)
        n += 1
    #plt.show()
    print(policy)
    fig = plt.figure()
    ax = plt.axes(xlim=(-6,6),ylim=(-6,6))
    line, = ax.plot([],[],color='r')
    line2, = ax.plot([],[],color='b')
    line3, = ax.plot([],[],color='b')
    plt.scatter(target_x, line_y, color='g')
    it_text = ax.text(4, 5, '',fontsize=10)
    def init():
        line1x = [0, x1[0], x2[0]]
        line1y = [0, y1[0], y2[0]]
        print(1)
        line.set_data(line1x, line1y)
        line2.set_data(x1[0], y1[0])
        line2.set_marker('o')
        line3.set_data(x2[0], y2[0])
        line3.set_marker('o')
        it_text.set_text('Iteration: %d' % (0))
        #m = int(sys.stdin.readline())
        return line, line2, line3, it_text,

    def animate(i):
        line1x = [0,x1[i],x2[i]]
        line1y = [0,y1[i],y2[i]]
        line.set_data(line1x,line1y)
        line2.set_data(x1[i],y1[i])
        line2.set_marker('o')
        line3.set_data(x2[i], y2[i])
        line3.set_marker('o')
        it_text.set_text('Iteration: %d'%(i))
        return line,line2,line3,it_text,
    ani = anim.FuncAnimation(fig,animate,range(len(x1)),init_func=init,interval=200,repeat=False)
    #ani.save('2-dof-arm.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    f = r"/Users/Jipeng/PycharmProjects/dopamine_rl/2-dof_video.mp4"
    writervideo = anim.FFMpegWriter(fps=60)
    ani.save(f, writer=writervideo)
    plt.show()




