'''
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
data = np.random.random((255, 255))
im = plt.imshow(data, cmap='gray')

# animation function.  This is called sequentially
def animate(i):
    data = np.random.random((255, 255))
    im.set_array(data)
    return [im]

anim = animation.FuncAnimation(fig, animate, frames=200, interval=60, blit=True)
plt.show()
'''

from __future__ import print_function
import torch
'''
x = torch.empty(5,3)
print (x)
y = torch.zeros(5,3,dtype=torch.long)
print (x[:,1])
z = x.view(-1,3)
a = z.numpy()
z.add_(1)
print (z)
print (a)
'''
'''
x = torch.ones(2,2,requires_grad=True)
print (x)
y = x + 2
print (y)
print (y.grad_fn)
z = y * y * 3
out = z.mean()
print (z, out)

a = torch.randn(2,2)
a = ((a*3)/(a-1))
print (a.requires_grad)
a.requires_grad_(True)
print (a.requires_grad)
b = (a*a).sum()
print (b.grad_fn)
out.backward()
print(x.grad)
'''
import sys
import cv2
import os
import numpy as np

video_src_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/data/video/'
image_src_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/data/images/'
file_name = '2-dof_video.mp4'
def frame_writer(videopath,imagepath):
    camera = cv2.VideoCapture(videopath)
    #width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    index = 0
    if not camera.isOpened():
        print ('Could not open video')
        sys.exit()
    while True:
        res, frame = camera.read()
        if not res:
            break
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #print hsv
        l_blue = np.array([100,43,46])
        h_blue = np.array([124,255,255])
        mask = cv2.inRange(hsv,l_blue,h_blue)
        res = cv2.bitwise_and(frame,frame,mask= mask)
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        cv2.waitKey(0)
frame_writer(video_src_path+'2-dof_video_0.mp4',None)