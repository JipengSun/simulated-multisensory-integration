import sys
import cv2
import os
import numpy as np

video_src_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/data/video/'
image_src_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/data/images/'
file_name = 'sample_video.avi'

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
        if index%2 == 0:
            image_name = 'img%s.jpg'% index
            cv2.imwrite(imagepath + image_name, frame)
        index += 1

frame_writer(video_src_path+file_name,image_src_path+'NAO/')