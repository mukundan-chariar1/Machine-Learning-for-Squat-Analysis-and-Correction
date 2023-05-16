import calib as cal
import os
import numpy as np
import sys
import save_parameters as save

if len(sys.argv) != 2:
    print('Call with settings filename: "python3 calibrate.py calibration_settings.yaml"')
    quit()

#Open and parse the settings file
cal.parse_calibration_settings_file(sys.argv[1])


"""Step1. Save calibration frames for single cameras"""
#cal.save_frames_single_camera('camera0') #save frames for camera0
#cal.save_frames_single_camera('camera1') #save frames for camera1

'''
"""Step2.A Obtain camera intrinsic matrices and save them"""
#camera0 intrinsics
images_prefix = os.path.join('frames', 'camera0*')
cmtx0, dist0 = cal.calibrate_camera_for_intrinsic_parameters(images_prefix) 
cal.save_camera_intrinsics(cmtx0, dist0, 'camera0') #this will write cmtx and dist to disk
#camera1 intrinsics
images_prefix = os.path.join('frames', 'camera1*')
cmtx1, dist1 = cal.calibrate_camera_for_intrinsic_parameters(images_prefix)
cal.save_camera_intrinsics(cmtx1, dist1, 'camera1') #this will write cmtx and dist to disk
'''
"""Step2.B Load camera intrinsic matrices"""
cmtx0, dist0=cal.load_cam_intrinsics('camera0')
cmtx1, dist1=cal.load_cam_intrinsics('camera1')

"""Step3. Save calibration frames for both cameras simultaneously"""
cal.save_frames_two_cams('camera0', 'camera1') #save simultaneous frames


"""Step4.A Use paired calibration pattern frames to obtain camera0 to camera1 rotation and translation"""
frames_prefix_c0 = os.path.join('frames_pair', 'camera0*')
frames_prefix_c1 = os.path.join('frames_pair', 'camera1*')
R, T = cal.stereo_calibrate(cmtx0, dist0, cmtx1, dist1, frames_prefix_c0, frames_prefix_c1)

"""Step4.B Load rotational and translational data"""
#R, T=cal.load_rot_trans_data('camera1')

"""Step5. Save calibration data where camera0 defines the world space origin."""
#camera0 rotation and translation is identity matrix and zeros vector
R0 = np.eye(3, dtype=np.float32)
T0 = np.array([0., 0., 0.]).reshape((3, 1))

cal.save_extrinsic_calibration_parameters(R0, T0, R, T) #this will write R and T to disk
R1 = R; T1 = T #to avoid confusion, camera1 R and T are labeled R1 and T1
#check your calibration makes sense
camera0_data = [cmtx0, dist0, R0, T0]
camera1_data = [cmtx1, dist1, R1, T1]
cal.check_calibration('camera0', camera0_data, 'camera1', camera1_data, _zshift = 1.)

sys.exit(save.save_parameters())

"""Optional. Define a different origin point and save the calibration data"""
# #get the world to camera0 rotation and translation
# R_W0, T_W0 = get_world_space_origin(cmtx0, dist0, os.path.join('frames_pair', 'camera0_4.png'))
# #get rotation and translation from world directly to camera1
# R_W1, T_W1 = get_cam1_to_world_transforms(cmtx0, dist0, R_W0, T_W0,
#                                           cmtx1, dist1, R1, T1,
#                                           os.path.join('frames_pair', 'camera0_4.png'),
#                                           os.path.join('frames_pair', 'camera1_4.png'),)

# #save rotation and translation parameters to disk
# save_extrinsic_calibration_parameters(R_W0, T_W0, R_W1, T_W1, prefix = 'world_to_') #this will write R and T to disk'''
