import os
import shutil
from datetime import datetime

def save_parameters():
    path_save='/home/mukundan/Desktop/VIII_SEM/Data/cam_parameters'
    path_load='/home/mukundan/Desktop/VIII_SEM/Repositories/python_stereo_camera_calibrate'

    now=datetime.now()
    stamp_file=now.strftime('%d%m%Y_%H%M%S')
    stamp_folder=now.strftime('%d%m%Y')

    folder_name='parameters_'+stamp_folder
    file_name_params='camera_parameters_'+stamp_file
    file_name_frames='frames_pair_'+stamp_file

    if os.path.exists(os.path.join(path_save, folder_name)):
        os.mkdir(os.path.join(os.path.join(path_save, folder_name), file_name_params))
        files=os.listdir(os.path.join(path_load, 'camera_parameters'))
        for file in files:
            shutil.copy(os.path.join(os.path.join(path_load, 'camera_parameters'), file), os.path.join(os.path.join(path_save, folder_name), file_name_params))
    else:
        os.mkdir(os.path.join(path_save, folder_name))
        os.mkdir(os.path.join(os.path.join(path_save, folder_name), file_name_params))
        files=os.listdir(os.path.join(path_load, 'camera_parameters'))
        for file in files:
            shutil.copy(os.path.join(os.path.join(path_load, 'camera_parameters'), file), os.path.join(os.path.join(path_save, folder_name), file_name_params))

    if os.path.exists(os.path.join(path_save, folder_name)):
        os.mkdir(os.path.join(os.path.join(path_save, folder_name), file_name_frames))
        files=os.listdir(os.path.join(path_load, 'frames_pair'))
        for file in files:
            shutil.copy(os.path.join(os.path.join(path_load, 'frames_pair'), file), os.path.join(os.path.join(path_save, folder_name), file_name_frames))
    else:
        os.mkdir(os.path.join(path_save, folder_name))
        os.mkdir(os.path.join(os.path.join(path_save, folder_name), file_name_frames))
        files=os.listdir(os.path.join(path_load, 'frames_pair'))
        for file in files:
            shutil.copy(os.path.join(os.path.join(path_load, 'frames_pair'), file), os.path.join(os.path.join(path_save, folder_name), file_name_frames))
    
