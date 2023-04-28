import os
import csv

#path_save='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'
path_save='/media/mukundan/MLSAC DRIVE/cam_recordings_firstset_copy'
#path_save='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings_done_2'

files=os.listdir(path_save)
#files =['recording_12042023_100738', 'recording_12042023_100731', 'recording_12042023_100627', 'recording_12042023_100717', 'recording_12042023_100636', 'recording_12042023_100651', 'recording_12042023_100644', 'recording_12042023_100724', 'recording_12042023_100658',]

with open(os.path.join(path_save, 'csvfile_lengths.csv'), 'w') as csvfile:
    outwriter=csv.writer(csvfile)
    for file in files:
        '''
        if not os.path.exists(os.path.join(os.path.join(path_save, file), 'label.txt')):
            with open(os.path.join(os.path.join(path_save, file), 'label.txt'), 'w') as label:
                label.write("powerlifting squats")
    '''
        if os.path.exists(os.path.join(os.path.join(path_save, file), 'kpts_3d.dat')):
            with open(os.path.join(os.path.join(path_save, file), 'kpts_3d.dat'), 'r') as label:
                label_line= label.readlines()
                #if label_line=='testing data': label.writeline('test data')
                #label.write('bending forward')
        else: label_line=''
        row=[file, len(label_line)]
        outwriter.writerow(row)






	