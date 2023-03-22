import csv
import inference_button_deep_edited as inf
import os
import pandas as pd
import sys

from Countpose_deep_edited import *

count=Countpose()

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)

path_data='/home/robotics/MLSAC Repositories/SquatClassificationAndCounting/edited/videos' #change the path here
path_csv='/home/robotics/MLSAC Repositories/SquatClassificationAndCounting/edited/output_csv' #change the path here

reader=pd.read_csv("input_csv.csv")
df=pd.DataFrame(reader)
placeholder=reader["name"].tolist()
print(placeholder)
names=['file', 'quarter', 'half', 'full', 'total', 'comments']

csv_headers = [
        'left_shoulder_x', 'left_shoulder_y',
        'right_shoulder_x', 'right_shoulder_y',
        'left_hip_x', 'left_hip_y',
        'right_hip_x', 'right_hip_y',
        'left_knee_x', 'left_knee_y',
        'right_knee_x', 'right_knee_y',
        'left_ankle_x', 'left_ankle_y',
        'right_ankle_x', 'right_ankle_y',
        'squat'
    ]
with open(os.path.join(path_csv, '4typeoutput.csv'), 'w') as output:
	outwriter = csv.writer(output)
	outwriter.writerow(names)
	for file in placeholder:
		print(file)
		filename = file[:-4]+'.csv'
		squats=[]
		total_squat=0
		with open(os.path.join(path_csv, filename), 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(csv_headers)
			csv_output_rows=[]
			squats=[0,0,0]
			total_squat=0
			try:
				
				file_path=path_data+'/'+file
				csv_output_rows, squats, total_squat=inf.start_squat(2, 0, file_path)
				print(squats)
			except:
				print('error')
				comment='error'
			else:
				comment='squat ok'
			csvwriter.writerows(csv_output_rows)
		row=[file, squats[0], squats[1], squats[2], total_squat, comment]
		outwriter.writerow(row)
		count.reset_squat_count()
			
