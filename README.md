# 1. Machine-Learning-for-Squat-Analysis-and-Correction

A squat is defined as an exercise in which a standing person lowers to a position in which the torso is erect and the knees are deeply bent and then returns to its original upright position. Squats are one of the most nuanced exercises. Each person will have a different type of squat as different individuals having their own unique length of limbs will cause their form to vary when observed. We also see that the mobility of different joints contributes to this, as well as the strength of their muscles. To assess  each  person  uniformly  and  fairly,  we  introduce  our  model  that  takes into  consideration  the relative distance travelled of each significant joint of their bodies to move such that they achieve their own  version  of  a  perfect  squat.  Hence  in  this  project  we  plan  to  use  machine  learning  to  analyze whether  the  person  doing  the squat to  the  best  of  their  abilities  according  to  their  body proportions. If there is room for improvement, then we attempt to identify where they can improve by visually showing the trainee their position versus their ideal position.

The goal of this project is to analyze people's form while performing squats and compare it to the ideal form of squats according to their body type. The aim is to help beginners correct and monitor their form to improve their progress. To achieve this, the project will use python and its libraries such as TensorFlow, PyTesseract and other machine vision modules. The project builds on existing work in  the  field  of  machine  vision  using  MATLAB  to  recognize  and  perform  motion  analysis  of compound exercises. The expected outcome of this project is to create a  program or interface that can take a video as an input and give an output as a video with the skeleton of the ideal squat. This will enable beginners to monitor their form and improve their progress in squat exercises.

# 2 Stereo Vision module

We use a Stereo vision calibration  module from Temuge Batpurev: https://github.com/TemugeB/python_stereo_camera_calibrate along with a pose estimation module that uses stereo vision from the same author: https://github.com/TemugeB/bodypose3d. They have been edited to our specifications. 

Stereo Vision is defined as the process of extracting 3D information from digital images taken by two cameras displaced horizontally from one another to obtain two different views of the same scene. We use stereo vision in this project in order to obtain more accurate pose information. We use a pair of Intel RealSense D435 Depth cameras. We mainly use the RGB module of the cameras. The mounts for the cameras were specifically 3D printed along with the mounting screws. The .f3d and the .stl file shall be made available on this page. 

## 2.1 Calibration

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

<img src='/media/camera0_0_single.png' width='25%' height='25%'><img src='/media/camera0_0.png' width='25%' height='25%'><img src='/media/camera1_0.png' width='25%' height='25%'>

## 2.2 Recording Videos in Stereo

Copy and paste the camera parameters into /bodypose3d/camera_parameters, then to record a video run the command:
```
python stereo_recorder.py
```

## 2.3 Converting to Pose Data

Direct Linear Transform (DLT) is a powerful technique in machine vision that enables 3D reconstruction and camera calibration. By utilizing a 2 camera setup, DLT can enhance these tasks and offer improved accuracy and depth perception.

DLT works by establishing correspondences between 3D points in the real world and their corresponding 2D projections in the image plane. The DLT method is based on singular value decomposition (SVD). With a 2 camera setup, two cameras capture the same scene from different viewpoints, providing additional information for depth estimation. Since the DLT method gives us a system of two equations for onr camera view, we must use a pair of cameras (or more) to estimate the world co-ordinates.

To convert videos into pose data, first we extract Landmarks frm the videos using MediaPipe. Then we use the camera parameters and DLT to estimate the world co-ordinates. The pose data is approximated to the real life proportions of the person in the video, compared to MediaPipes normalized data. 

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
<img src='/media/skeleton.png' width='50%' height='50%'>

### 2.3.1 Utilities

Under the /bodypose3d/utilities folder you will find some utilities to visualize the data and label it.

The codes are as follows:

- `csv_label_writer.py` - to make a csv with all the labels in it
- `csv_label_reader.py` - to visualize this data in the form of a chart
- `csv_length_writer.py` - to make a csv with the length of all the pose data in it
- `csv_length_reader.py` - to visualize this data in the form of a chart
- `label_writer.py` - to write labels to the collected data

# 3 MLSAC Module

We have classified squats according to seven types, them being:

- Wrong Types

    - bending forward
  
  ![](/media/bending_forward.gif 'Bending Forward') ![](/media/bending_forward_vid.gif 'Bending Forward')
    - heels lifting
  
  ![](/media/heels_lifting.gif 'Heels Lifting') ![](/media/heels_lifting_vid.gif 'Heels Lifting') 
    - knees caving
  
  ![](/media/knees_caving.gif 'Knees Caving') ![](/media/knees_caving_vid.gif 'Knees Caving') 
    - no depth
  
  ![](/media/no_depth.gif 'No Depth') ![](/media/no_depth_vid.gif 'No Depth')
    - toes lifting
  
  ![](/media/toes_lifting.gif 'Toes Lifting') ![](/media/toes_lifting_vid.gif 'Toes Lifting')

- Right Types

    - olympic squat
  
  ![](/media/olympic_squat.gif 'Olympic Squat') ![](/media/olympic_squat_vid.gif 'Olympic Squat')
    - powerlifting squat
  
  ![](/media/powerlifting_squat.gif 'Powerlifting Squat') ![](/media/powerlifting_squat_vid.gif 'Powerlifting Squat')

Currently, our dataset comprises 1292 videos. The visualization for the data is shown below.

|Type| Number|
|---|---|
|heels lifting| 177| 
|no depth| 182|
|knees caving| 152|
|bending forward| 163|
|toes lifting| 154|
|olympic squat| 264|
|powerlifting squat| 240|
| total| 1332|

<img src='/media/data_pie.png' width='100%' height='100%'>
<img src='/media/data_bars.png' width='100%' height='100%'>

## 3.1 Data Collection and Conversion

Under the /data_col_conv folder you will find:

- `data_cllector.py` - to collect all .dat files from individual folders and store it in the selected place. This also labels all files to the given label.
- `data_converter.py` -  to pad the data to the required length and convert the .dat file to a .npy file

## 3.2 Classification

We use a bidirectional LSTM model to classify the squats. The use of a bidirectional network allows us to gain more context for the data. The model is composed of:

- 3 Bidirectional LSTM layers
- 3 Dropout layers
- 3 Dense layers 
- 1 Flatten layer

<img src='/media/LSTM_092/model_LSTM.png'>

To train and test the model, run the `seq_classifier.ipynb` notebook. The notebook generates the confusion matrix for the classifier as well. Shown below are the confusion matrices for the same. The graphs for accuracy, val_accuracy and loss, val_loss over epochs is generated as well. 

<img src='/media/LSTM_092/confusion_matrix_LSTM.png' width='50%' height='50%'><img src='/media/LSTM_092/confusion_matrix_normalized_LSTM.png' width='50%' height='50%'>
<img src='/media/LSTM_092/model_accuracy_LSTM.png' width='50%' height='50%'><img src='/media/LSTM_092/model_loss_LSTM.png' width='50%' height='50%'>

The classifier is trained for a 1000 epochs with a learning rate of 0.001. The dropout layers are inserted with a coefficient of 0.2 in order to prevent overtraining. The callbacks given to this model are model_checkpoint, which saves the best model so far. We chose to save the best validation accuracy. The model trained boasts a 92% validation accuracy.

We also visualize each point that is extracted as a 3d graph using `squat_estimation/vis_squat.py`. You will have to edit the code a bit in order to view these graphs. 

Refer to [graphs.md](graphs.md) to see the 3d curves for each point on the body.

## 3.3 Estimation of Good Squat

Besides the classification of the given squat, we have also implemented estimation of a good squat, given the first detected set of landmarks via MediaPipe. We have used the approach of fitting a curve for each coordinate for each point of a squat, to each type of good squat. 

y=k<sub>0</sub> + k<sub>1</sub>x + k<sub>2</sub>x<sup>2</sup> + k<sub>3</sub>x<sup>3</sup> + ..... + k<sub>n-1</sub>x<sup>n-1</sup>

The logic begind this is that the curve for a coordinate remains the same, even for different individuals with different limb lengths. Only the constant 'k<sub>0</sub>' varies, hence the original estimate of coordinates is taken as the constant. 

Refer to [graphs.md](graphs.md) to see the curves fit.

You will find a few codes under /squat_estimation, these are used the estimate the proper squat for the person. 

To fit a curve to a squat, choose the squat you want to fit to, use `get_landmarks.py` to extract pose data directly from MediaPipe, then edit `curve_fit.py` and run it. It will generate a csv file that you must save under /squat_estimation/csv_coeffs. This contains the coefficients for the curve of the squat. 

In order to estimate the squat, we use scipy.optimize.curve_fit. This allows us to get the curve most appropriate to the person who is squatting. As explained previously, the 'k<sub>0</sub>' value changes for each person. This determines the starting point for coordinate of the squat. The curve is also stretched using simple timescaling, in order to show the comparison effectively. 

First, we extract the Landmarks using MediaPipe, and they are stored as `*landmarks.dat`. Then the starting point for the squat is selected, and the correct squat is estimated. This is saved as `*landmarks_est.dat`. The landmarks are converted to pixel values, and then converted to 3D world co-ordinates and saved as `kpts_3d_est.dat`. This file contains the final correct squat generated for the person, and will be shown side by side with the actual squat done. 

To convert the video of an improper squat into pose data directly extracted from MediaPipe, run: 

```
python get_landmarks.py <file name here>
```
Or if you want to convert all previously unconverted videos into pose data:
```
python get_landmarks.py seq
``` 

To generate the estimate of a good squat from a bad squat, run:

```
python squat_estimator.py <file name here>
```
Here you will have a choice between olympic and powerlifting squat, and the code will show the estimated MediaPipe pose data generated for either cameras, and then the data fit to the persons limb lengths using DLT. The estimated squat will be shown in green, while the actual squat will be shown in red.

![](/media/oly_gen.gif 'Olympic Squat Generated') ![](/media/pl_gen.gif 'Powerlifting Squat Generated')
