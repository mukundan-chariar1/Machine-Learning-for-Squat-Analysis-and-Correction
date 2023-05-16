import pandas as pd
import numpy as np
import os
import sys
import show_pose as show
from utils import DLT, get_projection_matrix, write_keypoints_to_disk

path_vids='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'

frame_shape = [1920, 1080]

# define the true objective function
def curve_oly(x, a, b, c, d, e, f, g, h, i, j, y1):
    return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f*x**6)+(g*x**7)+(h*x**8)+(i*x**9)+j +(y1-j)

def curve_pl(x, a, b, c, d, e, f, g, h, i, y1):
    return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + (f*x**6)+(g*x**7)+(h*x**8)+i +(y1-i)


def decompose(filename):
    
    k=input('1 for oly, 2 for pl\n-> ')

    if k=='1': 
        df_coeffs_cam0 = pd.read_csv('csv_coeffs/csv_coeffs_oly_1.csv')
        df_coeffs_cam1 = pd.read_csv('csv_coeffs/csv_coeffs_oly_2.csv')
    elif k=='2':
        df_coeffs_cam0 = pd.read_csv('csv_coeffs/csv_coeffs_pl_1.csv')
        df_coeffs_cam1 = pd.read_csv('csv_coeffs/csv_coeffs_pl_2.csv')
    else:
        sys.exit(print("error"))

    print(df_coeffs_cam0)
    print(df_coeffs_cam1)

    df_coeffs=[df_coeffs_cam0, df_coeffs_cam1]

    df_cam0=[]
    df_cam1=[]
    df_cam0=pd.DataFrame(df_cam0)
    df_cam1=pd.DataFrame(df_cam1)

    df_cams=[df_cam0, df_cam1]

    inp1=[0.467733711004257, 0.354782462120056, -0.275070250034332, 0.47819522023201, 0.367357194423676, -0.198983550071716, 0.450130432844162, 0.368006616830826, -0.210238218307495, 0.545417308807373, 0.411724388599396, -0.0484113320708275, 0.360643208026886, 0.405888319015503, -0.0760888978838921, 0.517278492450714, 0.458321869373322, -0.245568543672562, 0.448116719722748, 0.449536740779877, -0.276570409536362, 0.381921470165253, 0.429860770702362, -0.407191753387451, 0.570958614349365, 0.436304867267609, -0.387794017791748, 0.533317625522614, 0.595024585723877, -0.000661279307678342, 0.408691585063934, 0.598510503768921, 0.000713694316800684, 0.550748705863953, 0.728003859519959, -0.0616327933967114, 0.404696732759476, 0.729199647903442, 0.0257889200001955, 0.575164198875427, 0.838457584381104, 0.289028763771057, 0.400501579046249, 0.850424945354462, 0.328980058431625, 0.557501792907715, 0.851771712303162, 0.312504261732101, 0.412425965070725, 0.857942223548889, 0.346906036138535, 0.617910385131836, 0.896211445331574, 0.0802904590964317, 0.393934428691864, 0.908989787101746, 0.123508244752884]
    inp2=[0.441104114055634, 0.35981822013855, -0.33786216378212, 0.455914169549942, 0.373822778463364, -0.262678265571594, 0.419865548610687, 0.372758686542511, -0.259126096963882, 0.521771669387817, 0.412941545248032, -0.129686906933784, 0.351775139570236, 0.411651194095612, -0.0530162826180458, 0.495779156684876, 0.441827476024628, -0.393110752105713, 0.349982857704163, 0.443465530872345, -0.330854892730713, 0.365494549274445, 0.42423477768898, -0.550161242485046, 0.514529585838318, 0.44165712594986, -0.570097923278809, 0.495217502117157, 0.600588500499725, -0.0301261451095343, 0.37278163433075, 0.602197706699371, 0.0300476718693972, 0.512062847614288, 0.730381011962891, -0.0756196230649948, 0.371809810400009, 0.729269027709961, 0.128638684749603, 0.535833239555359, 0.845643997192383, 0.220627322793007, 0.35719308257103, 0.842043519020081, 0.43733137845993, 0.52802962064743, 0.856627345085144, 0.234955370426178, 0.374092131853104, 0.854195475578308, 0.455593794584274, 0.540486395359039, 0.905803382396698, -0.0069948541931808, 0.311662256717682, 0.907533764839172, 0.263423562049866]
    
    inp1=np.loadtxt(os.path.join(os.path.join(path_vids, filename),'kpts_cam0_landmarks.dat'))
    inp1=inp1.reshape(-1, 57)
    inp1_len=inp1.shape[0]
    inp1=inp1[3, :]
    
    inp2=np.loadtxt(os.path.join(os.path.join(path_vids, filename),'kpts_cam1_landmarks.dat'))
    inp2=inp2.reshape(-1, 57)
    inp2_len=inp2.shape[0]
    inp2=inp2[3, :]

    inp=[inp1, inp2]
    inp_len=[inp1_len, inp2_len]

    name=['kpts_cam0_landmarks_est.dat', 'kpts_cam1_landmarks_est.dat']

    for df in zip(df_coeffs, df_cams, inp, name, inp_len):
        for i_ in zip(df[0].index, df[2]):
            if k=='1':
                x_line = np.arange(0, 101, 1/df[4]*101)
                y_line = curve_oly(x_line, df[0]['a'][i_[0]], df[0]['b'][i_[0]], df[0]['c'][i_[0]], df[0]['d'][i_[0]], df[0]['e'][i_[0]], df[0]['f'][i_[0]], df[0]['g'][i_[0]], df[0]['h'][i_[0]], df[0]['i'][i_[0]], df[0]['j'][i_[0]], i_[1])
            else:
                x_line = np.arange(0, 125, 1/df[4]*125)
                y_line = curve_pl(x_line, df[0]['a'][i_[0]], df[0]['b'][i_[0]], df[0]['c'][i_[0]], df[0]['d'][i_[0]], df[0]['e'][i_[0]], df[0]['f'][i_[0]], df[0]['g'][i_[0]], df[0]['h'][i_[0]], df[0]['i'][i_[0]], i_[1])
            df[1][df[0]['key'][i_[0]]]=y_line
        print(df[1])

        vals=np.array(df[1]).reshape(-1, 57)

        print(vals)

        np.savetxt(os.path.join(os.path.join(path_vids, filename),df[3]), vals)

        vals=show.read_keypoints(os.path.join(os.path.join(path_vids, filename),df[3]))
        show.visualize_mp(vals)


def recompose(filename):

    landmarks_cam0=np.loadtxt(os.path.join(os.path.join(path_vids, filename),'kpts_cam0_landmarks_est.dat'))
    landmarks_cam1=np.loadtxt(os.path.join(os.path.join(path_vids, filename),'kpts_cam1_landmarks_est.dat'))
    landmarks_cam0=landmarks_cam0.reshape(-1, 19, 3)
    landmarks_cam1=landmarks_cam1.reshape(-1, 19, 3)

    kpts_3d=[]

    landmarks_lst=[landmarks_cam0, landmarks_cam1]

    name=['kpts_cam0_est.dat', 'kpts_cam1_est.dat']

    for i, landmarks in enumerate(landmarks_lst):
        cam_pxls=[]
        for row in landmarks:
            frame_pxls = []
            for landmark in row:
                pxl_x = landmark[0] * frame_shape[1]
                pxl_y = landmark[1] * frame_shape[0]
                pxl_x = int(round(pxl_x))
                pxl_y = int(round(pxl_y))
                pxls = [pxl_x, pxl_y]
                frame_pxls.append(pxls)
            cam_pxls.append(frame_pxls)

        write_keypoints_to_disk(os.path.join(os.path.join(path_vids, filename),name[i]), np.array(cam_pxls))

    cam0_pxls=np.loadtxt(os.path.join(os.path.join(path_vids, filename),name[0]))
    cam1_pxls=np.loadtxt(os.path.join(os.path.join(path_vids, filename),name[1]))

    P0 = get_projection_matrix(0)
    P1 = get_projection_matrix(1)

    for row1, row2 in zip(cam0_pxls, cam1_pxls):
        frame0_keypoints=row1.reshape(19, -1)
        frame1_keypoints=row2.reshape(19, -1)
        frame_p3ds = []
        for uv1, uv2 in zip(frame0_keypoints, frame1_keypoints):
            if uv1[0] == -1 or uv2[0] == -1:
                _p3d = [-1, -1, -1]
            else:
                _p3d = DLT(P0, P1, uv1, uv2) #calculate 3d position of keypoint
            frame_p3ds.append(_p3d)
        kpts_3d.append(frame_p3ds)

    write_keypoints_to_disk(os.path.join(os.path.join(path_vids, filename),'kpts_3d_est.dat'), kpts_3d)

    p3ds_act = show.read_keypoints(os.path.join(path_vids, os.path.join(filename, 'kpts_3d.dat')))
    p3ds_est = show.read_keypoints(os.path.join(path_vids, os.path.join(filename, 'kpts_3d_est.dat')))

    show.visualize_3d_vs(p3ds_act, p3ds_est)

if __name__=='__main__':
    filename=sys.argv[1]
    decompose(filename)
    recompose(filename)
    