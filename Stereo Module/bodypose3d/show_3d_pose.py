import numpy as np
import matplotlib.pyplot as plt
from utils import DLT
import os
import sys
plt.style.use('seaborn-v0_8-dark')

pose_keypoints = np.array([0, 9, 10, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])

path_kpts='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'

def read_keypoints(filename):
    fin = open(filename, 'r')

    kpts = []
    while(True):
        line = fin.readline()
        if line == '': break

        line = line.split()
        line = [float(s) for s in line]

        line = np.reshape(line, (len(pose_keypoints), -1))
        kpts.append(line)

    kpts = np.array(kpts)
    return kpts


def visualize_3d(p3ds):

    """Now visualize in 3D"""
    torso = [[3, 4] , [4, 10], [10, 9], [9, 3]]
    armr = [[4, 6], [6, 8]]
    arml = [[3, 5], [5, 7]]
    legr = [[10, 12], [12, 14]]
    legl = [[9, 11], [11, 13]]
    head = [[0, 1], [1, 2], [2, 0]]
    footl = [[13, 17], [17, 15], [15, 13]]
    footr = [[14, 16], [16, 18], [18, 14]]
    body = [torso, arml, armr, legr, legl, head, footr, footl]
    colors = ['red', 'blue', 'green', 'black', 'orange', 'yellow', 'purple', 'grey']

    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for framenum, kpts3d in enumerate(p3ds):
        if framenum%2 == 0: continue #skip every 2nd frame
        for bodypart, part_color in zip(body, colors):
            for _c in bodypart:
                ax.plot(xs = [kpts3d[_c[0],0], kpts3d[_c[1],0]], ys = [kpts3d[_c[0],1], kpts3d[_c[1],1]], zs = [kpts3d[_c[0],2], kpts3d[_c[1],2]], linewidth = 4, c = part_color)

        #uncomment these if you want scatter plot of keypoints and their indices.
        # for i in range(12):
        #     #ax.text(kpts3d[i,0], kpts3d[i,1], kpts3d[i,2], str(i))
        #     #ax.scatter(xs = kpts3d[i:i+1,0], ys = kpts3d[i:i+1,1], zs = kpts3d[i:i+1,2])


        #ax.set_axis_off()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        ax.set_xlim3d(-50, 50)
        ax.set_xlabel('x')
        ax.set_ylim3d(-50, 50)
        ax.set_ylabel('y')
        ax.set_zlim3d(-50, 50)
        ax.set_zlabel('z')
        plt.pause(0.1)
        ax.cla()


if __name__ == '__main__':

    p3ds = read_keypoints('kpts_3d.dat')

    if len(sys.argv) == 2:
        p3ds = read_keypoints(os.path.join(path_kpts, os.path.join((sys.argv[1]), 'kpts_3d.dat')))

    visualize_3d(p3ds)