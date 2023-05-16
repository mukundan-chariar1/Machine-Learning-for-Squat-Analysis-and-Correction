import os
import shutil

path_save='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'
path_load='/media/mukundan/MLSAC DRIVE/cam_recordings_firstset_copy'

files=os.listdir(path_load)

for file in files:
	if os.path.exists(os.path.join(os.path.join(path_load, file), 'label.txt')):
         with open(os.path.join(os.path.join(path_load, file), 'label.txt'), 'r') as label:
            lab=label.read()
            print(lab)
            if lab.startswith('olympic squat'):
                shutil.copytree(os.path.join(path_load, file), os.path.join(path_save, file))



   