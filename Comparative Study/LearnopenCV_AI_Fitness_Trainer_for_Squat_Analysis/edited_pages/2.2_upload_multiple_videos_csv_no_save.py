## This code eliminates streamlit as the medium, and is able to accept multiple videos as an input in the form of a csv. This code does not write to a csv file, it is only for presentation purposes



import csv
import cv2
import os
import sys
import pandas as pd
from utils import get_mediapipe_pose
from process_frame_edited import ProcessFrame
from thresholds import get_thresholds_beginner, get_thresholds_pro

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)

path_data='/home/mukundan/Desktop/VIII SEM/Data/Test' #change the path here
path_csv='/home/mukundan/Desktop/VIII SEM/Data/CSV_output' #change the path here

fieldnames=['state_seq','start_inactive_time','start_inactive_time_front','INACTIVE_TIME','INACTIVE_TIME_FRONT','DISPLAY_TEXT','COUNT_FRAMES','LOWER_HIPS','INCORRECT_POSTURE','prev_state','curr_state','SQUAT_COUNT','IMPROPER_SQUAT']


thresholds = None 

mode='Beginner' #for our convenience, we have used thresholds as beginner

if mode == 'Beginner':
    thresholds = get_thresholds_beginner() 

elif mode == 'Pro':
    thresholds = get_thresholds_pro()


upload_process_frame = ProcessFrame(thresholds=thresholds)

pose = get_mediapipe_pose()

output_video_file = f'output_recorded.mp4'

if os.path.exists(output_video_file):
    os.remove(output_video_file)

##reading the csf input file

reader=pd.read_csv("input_csv.csv")
df=pd.DataFrame(reader)
placeholder=reader["name"].tolist()
print(placeholder)

##initialising the cv2 module

vid=cv2.VideoCapture()


#for file in placeholder:

#reset the state tracker to its initial value
upload_process_frame.reset_state_tracker()

#create a file with the input files name as its name
#filename = file+'.csv'
#with open(os.path.join(path_csv, filename), 'w') as csvfile:
#csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
#csvwriter.writeheader()

try:
    vid=cv2.VideoCapture(path_data+'/'+file)

    # ---------------------  Write the processed video frame. --------------------
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_output = cv2.VideoWriter(output_video_file, fourcc, fps, frame_size)
    # -----------------------------------------------------------------------------

    if(vid.isOpened()==False):
        print("Error video not open")
    while(vid.isOpened()):
        ret, frame=vid.read()
        if(ret==True):
            cv2.imshow("frame", frame)
            if(cv2.waitKey(25) & 0xFF == ord('q')):
                break
            elif(cv2.waitKey(25) & 0xFF == ord('p')):
                cv2.waitKey(0)

        #convert frame from BGR to RGB before processing it.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out_frame, _ = upload_process_frame.process(frame, pose)
        state=upload_process_frame.return_state_tracker()
        print(upload_process_frame.return_state_tracker())
        #csvwriter.writerow(state)
        cv2.imshow("output frame", out_frame)
        video_output.write(out_frame[...,::-1])

except:
    print("error")

        
            
vid.release()
video_output.release()
cv2.destroyAllWindows()