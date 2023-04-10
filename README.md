# Machine-Learning-for-Squat-Analysis-and-Correction

A squat is defined as an exercise in which a standing person lowers to a position in which the torso is erect and the knees are deeply bent and then returns to its original upright position. Squats are one of the most nuanced exercises. Each person will have a different type of squat as different individuals having their own unique length of limbs will cause their form to vary when observed. We also see that the mobility of different joints contributes to this, as well as the strength of their muscles. To assess  each  person  uniformly  and  fairly,  we  introduce  our  model  that  takesinto  consideration  the relative distance travelled of each significant joint of their bodies to move such that they achieve their own  version  of  a  perfect  squat.  Hence  in  this  project  we  plan  to  use  machine  learning  to  analyze whether  the  person  doing  thequat  is  doing  to  the  best  of  their  abilities  according  to  their  body proportions. If there is room for improvement, then we attempt to identify where they can improve by visually showing the trainee their position versus their ideal position.

The goal ofthis project is to analyze people's form while performing squats and compare it to the ideal form of squats according to their body type. The aim is to help beginners correct and monitor their form to improve their progress. To achieve this, the project will use python and its libraries such as TensorFlow, PyTesseract and other machine vision modules. The project builds on existing work in  the  field  of  machine  vision  using  MATLAB  to  recognize  and  perform  motion  analysis  of compound exercises. The expected outcome of this project is to create a  program or interface that can take a video as an input and give an output as a video with the skeleton of the ideal squat. This will enable beginners to monitor their form and improve their progress in squat exercises.

# Stereo Vision module
We use a Stereo vision calibration  module from Temuge Batpurev: https://github.com/TemugeB/python_stereo_camera_calibrate along with a pose estimation module that uses stereo vision from the same author: https://github.com/TemugeB/bodypose3d. They have been edited to our specifications. 

Stereo Vision is defined as the process of extracting 3D information from digital images taken by two cameras displaced horizontally from one another to obtain two different views of the same scene. We use stereo vision in this project in order to obtain more accurate pose information. We use a pair of Intel RealSense D435 Depth cameras. We mainly use the RGB module of the cameras. The mounts for the cameras were specifically 3D printed along with the mounting screws. The f3d and the stl file shall be made available on this page. 

Attach the cameras individually and check which video feed has the cameras linked to it by using the command:
```
ls /dev/video*
```
In calibration_settings.yaml, change the camera numbers for camera0 and camera1, and the resolution in frame_width and frame_height to your cameras properties. Change the checkerboard_rows and checkerboard_columns as well, along with checkerboard_box_size_scale. 

To calibrate the cameras, run the command:
```
python calib_test.py calibration_settings.yaml
```
Before running this command, make sure all the steps that are necessary are uncommented. You can load a previous calibration as well. 

Copy and paste the camera parameters into /bodypose3d/camera_parameters, then to record a video run the command:
```
python stereo_recorder.py
```
To convert stereo recordings into pose data, run the command:
```
python bodypose3d.py <file name here>
```
Or if you want to convert all previously unconverted videos into pose data:
```
python bodypose3d.py seq
``` 
To view the pose data in skeleton format:
```
python show_3d_pose.py <file name here>
```
