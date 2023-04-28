import numpy as np
import os

path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/npy_files_seq/seq_og/oly'

data_list=os.listdir(path_save)
os.mkdir(os.path.join(path_save, 'seq_offset'))

print(len(data_list))

type_list=[]

for data in data_list:
    if data=='seq_beg' or data=='seq' or data=='seq_offset': continue
    #file=np.load(os.path.join(path_save, data))
    #file=np.fromfile(os.path.join(path_save, data), dtype='.dat')
    filename=data[:-4]+'_offset.npy'
    #np.save(os.path.join(path_save, filename), file)
    #print(file.dtype)
    #type_list.append(file.dtype)
    file=np.load(os.path.join(path_save, data))
    file=file[1:, :]
    shape=file.shape
    shape_neg=300-shape[0]
    file=np.pad(file, [(0, 1), (0, 0)], mode='constant', constant_values=-1.0)
    #np.save(os.path.join(path_save, filename), file)
    np.save(os.path.join(os.path.join(path_save, 'seq_offset'), filename), file )


#print(len(data_list))
#print(type_list)
'''
import numpy as np
import os

path_save='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/npy_files'

file=np.load(os.path.join(path_save, 'bending_forward_recording_05042023_125502.npy'))
print(file.dtype)
'''