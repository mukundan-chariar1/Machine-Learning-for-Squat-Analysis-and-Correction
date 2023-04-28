
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

plt.style.use('seaborn-v0_8-dark')

path_save='/media/mukundan/MLSAC DRIVE/cam_recordings_firstset_copy'

#files=os.listdir(path_save)
#print(files)

nums=[0, 0, 0, 0, 0, 0, 0]

with open(os.path.join(path_save,'csvfile.csv'), 'r') as csvfile:
    csvreader=csv.reader(csvfile)
    for row in csvreader:
        label_line= row[1]
        if label_line:
            if label_line=='heels lifting\n' or label_line=='heels lifting': nums[0]+=1
            elif label_line=='no depth\n' or label_line=='no depth': nums[1]+=1
            elif label_line=='knees caving\n' or label_line=='knees caving': nums[2]+=1
            elif label_line=='bending forward\n' or label_line=='bending forward': nums[3]+=1
            elif label_line=='toes lifting\n' or label_line=='toes lifting': nums[4]+=1
            elif label_line=='olympic squat\n' or label_line=='olympic squat': nums[5]+=1
            elif label_line=='powerlifting squat\n' or label_line=='powerlifting squat': nums[6]+=1
            else: continue

# creating the dataset
data = {'heels lifting':nums[0], 'no depth':nums[1], 'knees caving':nums[2],
        'bending forward':nums[3], 'toes lifting':nums[4], 'olympic squat':nums[5], 'powerlifting squat':nums[6]}

print(data)
courses = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (100, 7))
 
# creating the bar plot
#plt.bar(x = courses,y =  values, color ='maroon',
#        width = 0.4)
plt.pie(values, labels=courses)
 
plt.xlabel("Types of squats")
plt.ylabel("No. of squats")
plt.title("Squat Data")
plt.show()