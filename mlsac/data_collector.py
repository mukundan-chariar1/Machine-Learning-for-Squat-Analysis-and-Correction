import os
import sys
import shutil


path_load='/media/mukundan/MLSAC DRIVE/cam_recordings_firstset_copy'
#path_load='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'
path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data'

data_list=os.listdir(path_load)

for data in data_list:
    if data.startswith('csv'): continue
    with open(os.path.join(os.path.join(path_load, data), 'label.txt'), 'r') as label:
        label_type=label.readline()
        label_type=label_type.strip()
        label_type=label_type.replace(' ', '_')
    source=os.path.join(os.path.join(path_load, data), 'kpts_3d.dat')
    destination_name=label_type+'_'+data+'.dat'
    destination=os.path.join(path_save, destination_name)

    shutil.copy(source, destination)