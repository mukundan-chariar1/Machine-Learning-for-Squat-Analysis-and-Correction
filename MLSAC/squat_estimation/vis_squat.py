import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
import seaborn as sns

class VisSquat():
    
    def __init__(self):
        self.path_load='/home/mukundan/Desktop/VIII_SEM/Data/labelled_data/mp/npy/'
        self.seq_og=os.path.join(self.path_load, 'cam1_clean')

        self.data_list_seq_og=os.listdir(self.seq_og)
        self.data_list_seq_og.sort()

        self.kpts={'0_x':[], '0_y':[], '0_z':[],
            '1_x':[], '1_y':[], '1_z':[],
            '2_x':[], '2_y':[], '2_z':[],
            '3_x':[], '3_y':[], '3_z':[],
            '4_x':[], '4_y':[], '4_z':[],
            '5_x':[], '5_y':[], '5_z':[],
            '6_x':[], '6_y':[], '6_z':[],
            '7_x':[], '7_y':[], '7_z':[],
            '8_x':[], '8_y':[], '8_z':[],
            '9_x':[], '9_y':[], '9_z':[],
            '10_x':[], '10_y':[], '10_z':[],
            '11_x':[], '11_y':[], '11_z':[],
            '12_x':[], '12_y':[], '12_z':[],
            '13_x':[], '13_y':[], '13_z':[],
            '14_x':[], '14_y':[], '14_z':[],
            '15_x':[], '15_y':[], '15_z':[],
            '16_x':[], '16_y':[], '16_z':[],
            '17_x':[], '17_y':[], '17_z':[],
            '18_x':[], '18_y':[], '18_z':[],
            'i':[], 'name':[]}
        self.df=pd.DataFrame(self.kpts)

    def transpose_dat(self, file, filename):
        file=np.transpose(file)
        keys=self.kpts.keys()
        for i, key in enumerate(keys):
            if key=='i' or key=='name': continue
            self.kpts[key]=file[i,:]
        self.kpts['i']=list(range(0, len(self.kpts['0_x'])))
        self.kpts['name']=[filename]*len(self.kpts['0_x'])
        df_temp=pd.DataFrame(self.kpts)
        self.df=pd.concat([self.df, df_temp])
        return

    def get_dat(self):
        pbar=tqdm(total=len(self.data_list_seq_og))
        keys=self.kpts.keys()
        for i, data in enumerate(self.data_list_seq_og):
            pbar.update(1)
            open_f=np.load(os.path.join(self.seq_og, data))
            self.transpose_dat(file=open_f, filename=data)            
        pbar.close()
        return self.df

    def load_graph(self):
        for key in self.kpts.keys():
            if key=='i' or key=='name': continue
            start, end =0,0
            ax=plt.figure()
            plt.title(key)
            plt.xlabel('time')
            plt.ylabel(key)
            plt.grid()
            for i, j in enumerate(self.df['i']):
                if j==0 and i!=0: 
                    end=i-1
                    load_key=self.df[key][start:end]
                    y=list(range(0, len(load_key)))
                    plt.scatter(y=load_key, x=y)
                    start=end
            save_name=key+'.png'
            plt.savefig(save_name)
            plt.show()

    def load_graph_3d(self):
        key_lst=list(self.kpts.keys())[:-2]
        grp=[]
        key_lst_n=[]
        for i, key in enumerate(key_lst):
            grp.append(key)
            if i%3==2:
                key_lst_n.append(grp)
                grp=[]
        key_lst=key_lst_n
        for num, keys in enumerate(key_lst):
            fig=plt.figure()
            ax = plt.axes(projection='3d')
            plt.title(num)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.ylabel('z')
            plt.grid()
            x=[]
            y=[]
            z=[]
            for key in keys:
                start=0
                end=0
                for i, j in enumerate(list(self.df['i'])):
                    if j==0 and i!=0: 
                        end=i-1
                        load_key=list(self.df[key][start:end])
                        load_key=list(filter((-1.0).__ne__, load_key))
                        start=end
                        if str(key).endswith('x'): x.append(load_key)
                        elif str(key).endswith('y'): y.append(load_key)
                        elif str(key).endswith('z'): z.append(load_key)
            for xyz in zip(x, y, z):
                ax.plot(xyz[0], xyz[1], xyz[2])
            plt.savefig(os.path.join('imgs', str(key[:-2]+'.png')))
            plt.close()

    def load_graph_3d_full(self):
        key_lst=list(self.kpts.keys())[:-2]
        grp=[]
        key_lst_n=[]
        for i, key in enumerate(key_lst):
            grp.append(key)
            if i%3==2:
                key_lst_n.append(grp)
                grp=[]
        key_lst=key_lst_n
        fig=plt.figure()
        ax = plt.axes(projection='3d')
        plt.title('squat cloud')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.ylabel('z')
        plt.grid()
        for num, keys in enumerate(key_lst):
            x=[]
            y=[]
            z=[]
            for key in keys:
                start=0
                end=0
                for i, j in enumerate(list(self.df['i'])):
                    if j==0 and i!=0: 
                        end=i-1
                        load_key=list(self.df[key][start+4:end])
                        start=end
                        if str(key).endswith('x'): x.append(load_key)
                        elif str(key).endswith('y'): y.append(load_key)
                        elif str(key).endswith('z'): z.append(load_key)
            for xyz in zip(x, y, z):
                ax.plot3D(xyz[0], xyz[1], xyz[2])
        plt.show()

    def load_graph_3d_full_preds(self, preds):
        preds=np.array(preds)
        preds=preds.flatten().reshape(-1, 3)
        fig=plt.figure()
        ax = plt.axes(projection='3d')
        plt.title('squat cloud')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.ylabel('z')
        plt.grid()
        for crds in preds:
            crds=crds.flatten()
            print(crds)
            ax.scatter(crds[0], crds[1], crds[2])
        plt.show()


    def get_dat_3d(self, key):
        start=0
        end=0
        print(list(self.df['i']))
        for i, j in enumerate(self.df['i']):
            print(key)
            if j==0 and i!=0: 
                end=i-1
                load_key=list(self.df[key][start:end]) #[start+3:end] to ignore 1
                print(str(key).endswith('x'))
                if str(key).endswith('x'): x=load_key
                elif str(key).endswith('y'): y=load_key
                elif str(key).endswith('z'): z=load_key
                start=end

    def show_acc(self, history):
        plt.plot(history.history['accuracy'], marker='.')
        plt.plot(history.history['val_accuracy'], marker='.')
        plt.title('model accuracy')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.grid()
        plt.legend(['acc', 'val_acc'], loc='lower right')
        #plt.savefig(os.path.join(path_save, 'model_accuracy_lstm_6.png'))
        #plt.close()
        plt.show()
          
    def show_loss(self, history):
        plt.plot(history.history['loss'], marker='.')
        plt.plot(history.history['val_loss'], marker='.')
        plt.title('model loss')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.grid()
        plt.legend(['loss', 'val_loss'], loc='upper right')
        #plt.savefig(os.path.join(path_save, 'model_loss_lstm_6.png'))
        #plt.close()
        plt.show()

if __name__=='__main__': 
    vis=VisSquat()
    df=VisSquat.get_dat(vis)
    vis.load_graph_3d()
    """ vis=VisSquat()
    vis.load_graph_3d_full_preds() """