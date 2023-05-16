import numpy as np
import os
from tqdm import tqdm

#path_load='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/mp/pl/dat/cam1'
#path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/mp/pl/npy/cam1'

path_load='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/dat_files'
path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/npy_files'

data_list=os.listdir(path_load)

pbar=tqdm(total=len(data_list))

for data in data_list:
    pbar.update(1)
    file=np.loadtxt(os.path.join(path_load, data))
    #file=np.fromfile(os.path.join(path_save, data), dtype='.dat')
    filename=data[:-4]+'.npy'
    shape=file.shape
    shape_neg=300-shape[0]
    file=np.pad(file, [(0, shape_neg), (0, 0)], mode='constant', constant_values=-1.0)
    np.save(os.path.join(path_save, filename), file)
    #np.save(os.path.join(os.path.join(path_save, 'seq_offset'), filename), file )
    #np.save(os.path.join(path_save, filename), file[4:])


#print(len(data_list))
#print(type_list)
'''
import numpy as np
import os

path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/npy_files'

file=np.load(os.path.join(path_save, 'bending_forward_recording_05042023_125502.npy'))
print(file.dtype)
'''