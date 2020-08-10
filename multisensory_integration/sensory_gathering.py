import sys
import cv2

src_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/data/video/'
file_name = '2-dof_video.mp4'
full_path = src_path+file_name
def camera_detect(device):
    camera = cv2.VideoCapture(device)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if not camera.isOpened():
        print ('Could not open camera')
        sys.exit()
    while True:
        res, frame = camera.read()
        if not res:
            break
        cv2.imshow('detection',frame)
        cv2.waitKey(0)

def video2images(idx):
    file_path = src_path + '2-dof_video_%s.mp4' % idx
    camera_detect(device=file_path)
if __name__ == '__main__':
    for i in range(1,3):
        video2images(i)
