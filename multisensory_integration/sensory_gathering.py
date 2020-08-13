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
        image_name = 'img%s.jpg'% index
        cv2.imwrite(imagepath + image_name, frame)
        index += 1
        '''
        cv2.imshow('detection',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

# Convert the video to images. Frames in the same video will be saved into same folder.
def video2images(idx):
    video_path = video_src_path + '2-dof_video_%s.mp4' % idx
    image_folder_path = image_src_path +'original/' +str(idx)
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)
    frame_writer(video_path,image_folder_path + '/')

 # Clear all the files and directories under the root folder.
def delete_cascade(root_path):
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
def mask_frame_writer(videopath,imagepath):
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
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # print hsv
        l_blue = np.array([100, 43, 46])
        h_blue = np.array([124, 255, 255])
        mask = cv2.inRange(hsv, l_blue, h_blue)
        #res = cv2.bitwise_and(frame, frame, mask=mask)
        image_name = 'mask%s.jpg' % index
        cv2.imwrite(imagepath + image_name, mask)
        index += 1

def video2mask(idx):
    video_path = video_src_path + '2-dof_video_%s.mp4' % idx
    image_folder_path = image_src_path +'mask/'+ str(idx)
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path)
    mask_frame_writer(video_path,image_folder_path + '/')
if __name__ == '__main__':
    '''
    # Convert original frames
    delete_cascade(image_src_path+'original/')
    for i in range(50):
        video2images(i)
        print ('Video %s is converted'%i)
    '''
    # Convert mask frames
    delete_cascade(image_src_path+'mask/')
    for i in range(50):
        video2mask(i)
        print ('Video %s is converted to masked images' % i)
