
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

plt.style.use('seaborn-v0_8-dark')

path_save='/media/mukundan/MLSAC DRIVE/cam_recordings_firstset_copy'

#files=os.listdir(path_save)
#print(files)

nums=[0, 0, 0, 0, 0, 0, 0]

line=[]

with open(os.path.join(path_save,'csvfile_lengths.csv'), 'r') as csvfile:
    csvreader=csv.reader(csvfile)
    for row in csvreader:
        label_line= int(row[1])
        line.append(label_line)

line.sort()
print(line)

a = np.array(line)
 
# Creating histogram
fig, ax = plt.subplots(figsize =(10, 7))
ax.hist(a, bins=20)#bins = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300])

plt.xlabel("Data Lengths")
plt.ylabel("Number of Data")
plt.title("Data Lengths")
plt.savefig('data_bars.png')
# Show plot
plt.show()