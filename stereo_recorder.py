import cv2
import os
from datetime import datetime


def takevid():
    path_vids='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'
    out_name0='cam0.avi'
    out_name1='cam1.avi'

    now=datetime.now()
    stamp=now.strftime('%d%m%Y_%H%M%S')

    folder='recording_'+stamp
    path_save=os.path.join(path_vids, folder)
    os.mkdir(path_save)

    print(os.listdir(path_save))
    frame_shape = [1920, 1080]

    cap0=cv2.VideoCapture(6)
    cap1=cv2.VideoCapture(12)
    caps=(cap0, cap1)

    for cap in caps:
        cap.set(3, frame_shape[1])
        cap.set(4, frame_shape[0])

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    fps0 = cap0.get(cv2.CAP_PROP_FPS)
    out0 = cv2.VideoWriter(os.path.join(path_save, out_name0), fourcc, 30, (int(cap0.get(4)), int(cap0.get(3))))

    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    out1 = cv2.VideoWriter(os.path.join(path_save, out_name1), fourcc, 30, (int(cap1.get(4)), int(cap1.get(3))))

    cv2.namedWindow('cam0', cv2.WINDOW_KEEPRATIO)
    cv2.namedWindow('cam1', cv2.WINDOW_KEEPRATIO)

    cv2.resizeWindow('cam0',int(frame_shape[1]/2), int(frame_shape[0]/2))
    cv2.resizeWindow('cam1',int(frame_shape[1]/2), int(frame_shape[0]/2))

    if (cap0.isOpened() == False):
        print("Error opening the video file")
    while True:
        ret0, frame0=cap0.read()
        ret1, frame1=cap1.read()

        frame0=cv2.rotate(frame0,cv2.ROTATE_90_CLOCKWISE)   #code added for rotation
        frame1=cv2.rotate(frame1,cv2.ROTATE_90_CLOCKWISE)   #code added for rotation

        if ret1 == True and ret0 == True:
            out0.write(frame0)
            out1.write(frame1)
            cv2.imshow('cam0', frame0)
            cv2.imshow('cam1', frame1)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break

    cap0.release()
    out0.release()
    cap1.release()
    out1.release()
    cv2.destroyAllWindows()

    return

if __name__=='__main__':
    while True:
        takevid()
        key=ord(input('Would you like to take nother vid? \n -> '))
        if key & 0xFF == ord('y'):
            continue
        else:
            break
