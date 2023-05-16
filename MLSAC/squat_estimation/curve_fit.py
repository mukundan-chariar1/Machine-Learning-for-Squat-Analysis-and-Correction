
# fit a line to the economic data
from numpy import arange
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from vis_squat import VisSquat
import csv
import os

from time import sleep

vis=VisSquat()

df=vis.get_dat()
df=df.drop(labels=['i', 'name'], axis=1)
 
# define the true objective function
def objective(x, a, b, c, d, e, f, g, h, i):
    return (a*x) + (b*x**2) + (c*x**3) + (d*x**4) + (e*x**5) + (f*x**6) + (g*x**7) + (h*x**8) + i


with open('csv_coeffs.csv', 'w') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['key', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])
    for key in vis.kpts.keys():
        if key=='i' or key=='name': continue
        start, end =0, 0
        x=[]
        y=[]
        ax=plt.figure()
        plt.title(key)
        plt.xlabel('Time')
        plt.ylabel(key)
        plt.grid()
        for i_, j_ in enumerate(vis.df['i']):
            if j_==0 and i_!=0: 
                end=i_-1
                load_key=vis.df[key][start:end]
                x.extend(list(range(0, len(load_key))))
                y.extend(load_key)
                start=end

        popt, _ = curve_fit(objective, x, y)
        a, b, c, d, e, f, g, h, i= popt
        plt.plot(y, label='actual')
        x_line = arange(min(x), max(x), 1)
        y_line = objective(x_line, a, b, c, d, e, f, g, h, i)
        plt.plot(y_line, '--', color='red', label='estimated')
        plt.legend()
        plt.savefig(os.path.join('imgs', str(key+'.png')))
        #plt.show()
        print(key)
        print(a, b, c, d, e, f, g, h, i)
        writer.writerow([key, a, b, c, d, e, f, g, h, i])
        plt.close()
        """ z=input('continue?')
        if z=='y': 
            print(key)
            print(a, b, c, d, e, f, g, h, i, j)
            writer.writerow([key, a, b, c, d, e, f, g, h, i, j])
            continue
        else: break """

