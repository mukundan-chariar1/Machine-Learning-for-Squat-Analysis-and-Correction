import cv2 as cv
import mediapipe as mp
import numpy as np
import sys
from utils import DLT, get_projection_matrix
from utils import  write_keypoints_to_disk_edited as write_keypoints_to_disk
from datetime import datetime
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

frame_shape = [1920, 1080]

path_vids='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'

#add here if you need more keypoints
pose_keypoints = [16, 14, 12, 11, 13, 15, 24, 23, 25, 26, 27, 28, 29, 30, 31, 32, 0, 10, 9]

def run_mp(input_stream1, input_stream2):
    #input video stream
    cap0 = cv.VideoCapture(input_stream1)
    cap1 = cv.VideoCapture(input_stream2)
    caps = [cap0, cap1]

    cv.namedWindow('cam0', cv.WINDOW_KEEPRATIO)
    cv.namedWindow('cam1', cv.WINDOW_KEEPRATIO)

    cv.resizeWindow('cam0',int(frame_shape[1]/2), int(frame_shape[0]/2))
    cv.resizeWindow('cam1',int(frame_shape[1]/2), int(frame_shape[0]/2))

    #set camera resolution if using webcam to 1280x720. Any bigger will cause some lag for hand detection
    for cap in caps:
        cap.set(3, frame_shape[1])
        cap.set(4, frame_shape[0])

    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    j = 0

    #create body keypoints detector objects.
    pose0 = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pose1 = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    #containers for detected keypoints for each camera. These are filled at each frame.
    #This will run you into memory issue if you run the program without stop
    kpts_cam0 = []
    kpts_cam1 = []
    kpts_3d = []

    while True:

        #read frames from stream
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()

        if j<length: j+=1
        else: break

        #frame0=cv.rotate(frame0,cv.ROTATE_90_CLOCKWISE)   #code added for rotation
        #frame1=cv.rotate(frame1,cv.ROTATE_90_CLOCKWISE)   #code added for rotation

        #crop to 720x720.
        #Note: camera calibration parameters are set to this resolution.If you change this, make sure to also change camera intrinsic parameters
        if frame0.shape[1] != 720:
            frame0 = frame0[:,frame_shape[1]//2 - frame_shape[0]//2:frame_shape[1]//2 + frame_shape[0]//2]
            frame1 = frame1[:,frame_shape[1]//2 - frame_shape[0]//2:frame_shape[1]//2 + frame_shape[0]//2]

        # the BGR image to RGB.
        frame0 = cv.cvtColor(frame0, cv.COLOR_BGR2RGB)
        frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame0.flags.writeable = False
        frame1.flags.writeable = False
        results0 = pose0.process(frame0)
        results1 = pose1.process(frame1)

        #reverse changes
        frame0.flags.writeable = True
        frame1.flags.writeable = True
        frame0 = cv.cvtColor(frame0, cv.COLOR_RGB2BGR)
        frame1 = cv.cvtColor(frame1, cv.COLOR_RGB2BGR)

        #check for keypoints detection
        frame0_keypoints = []
        if results0.pose_landmarks:
            for i, landmark in enumerate(results0.pose_landmarks.landmark):
                if i not in pose_keypoints: continue #only save keypoints that are indicated in pose_keypoints
                pxl_x = landmark.x * frame0.shape[1]
                pxl_y = landmark.y * frame0.shape[0]
                crd_x = landmark.x
                crd_y = landmark.y
                crd_z = landmark.z
                pxl_x = int(round(pxl_x))
                pxl_y = int(round(pxl_y))
                cv.circle(frame0,(pxl_x, pxl_y), 3, (0,0,255), -1) #add keypoint detection points into figure
                kpts = [crd_x, crd_y, crd_z]
                frame0_keypoints.append(kpts)
                
        else:
            #if no keypoints are found, simply fill the frame data with [-1,-1] for each kpt
            frame0_keypoints = [[-1, -1, -1]]*len(pose_keypoints)

        #this will keep keypoints of this frame in memory
        kpts_cam0.append(frame0_keypoints)
        
        frame1_keypoints = []
        if results1.pose_landmarks:
            for i, landmark in enumerate(results1.pose_landmarks.landmark):
                if i not in pose_keypoints: continue
                pxl_x = landmark.x * frame1.shape[1]
                pxl_y = landmark.y * frame1.shape[0]
                crd_x = landmark.x
                crd_y = landmark.y
                crd_z = landmark.z
                pxl_x = int(round(pxl_x))
                pxl_y = int(round(pxl_y))
                cv.circle(frame1,(pxl_x, pxl_y), 3, (0,0,255), -1)
                kpts = [crd_x, crd_y, crd_z]
                frame1_keypoints.append(kpts)

        else:
            #if no keypoints are found, simply fill the frame data with [-1,-1] for each kpt
            frame1_keypoints = [[-1, -1, -1]]*len(pose_keypoints)

        #update keypoints container
        kpts_cam1.append(frame1_keypoints)

        if ret0 and ret1:
            cv.imshow('cam1', frame1)
            cv.imshow('cam0', frame0)

        k = cv.waitKey(1)
        if k & 0xFF == 27: break #27 is ESC key.


    cv.destroyAllWindows()
    cap0.release()
    #cap1.release()


    return np.array(kpts_cam0), np.array(kpts_cam1)

def seq_reader():
    folders=os.listdir(path_vids)
    for folder in folders:
        path_saved=os.path.join(path_vids, folder)
        vids=os.listdir(path_saved)
        if os.path.isfile(os.path.join(path_saved, 'kpts_3d_est.dat')): continue
        input_stream1 = os.path.join(path_saved, 'cam0.avi')
        input_stream2 = os.path.join(path_saved, 'cam1.avi')
        kpts_cam0, kpts_cam1 = run_mp(input_stream1, input_stream2)

        kpts_cam0_name=os.path.join(path_saved,'kpts_cam0_landmarks.dat')
        kpts_cam1_name=os.path.join(path_saved,'kpts_cam1_landmarks.dat')

        #this will create keypoints file in current working folder
        write_keypoints_to_disk(kpts_cam0_name, kpts_cam0)
        write_keypoints_to_disk(kpts_cam1_name, kpts_cam1)
        #key=ord(input('Would you like to continue:\n-> '))
        #if key & 0xFF == ord('y'): continue
        #else: break

    sys.exit()
            


if __name__ == '__main__':

    #this will load the sample videos if no camera ID is given
    input_stream1 = 'media/cam0_test.mp4'
    input_stream2 = 'media/cam1_test.mp4'

    #put camera id as command line arguements
    if sys.argv[1]=='seq':
        seq_reader()
    elif len(sys.argv) == 3:
        input_stream1 = int(sys.argv[1])
        #input_stream2 = int(sys.argv[2])
    elif len(sys.argv) == 2 :
        path_saved=os.path.join(path_vids, sys.argv[1])
        vids=os.listdir(path_saved)
        input_stream1 = os.path.join(path_saved, 'cam0.avi')
        input_stream2 = os.path.join(path_saved, 'cam1.avi')

    while True:

        kpts_cam0, kpts_cam1 = run_mp(input_stream1, input_stream2)

        kpts_cam0_name=os.path.join(path_saved,'kpts_cam0_landmarks.dat')
        kpts_cam1_name=os.path.join(path_saved,'kpts_cam1_landmarks.dat')

        #this will create keypoints file in current working folder
        write_keypoints_to_disk(kpts_cam0_name, kpts_cam0)
        write_keypoints_to_disk(kpts_cam1_name, kpts_cam1)

        key=ord(input('Would you like to take another vid:\n-> '))
        if key & 0xFF == ord('y'):
            path_saved=os.path.join(path_vids, input('enter the directory:\n-> '))
            vids=os.listdir(path_saved)
            input_stream1 = os.path.join(path_saved, 'cam0.avi')
            input_stream2 = os.path.join(path_saved, 'cam1.avi')
            continue
        else:
            break

