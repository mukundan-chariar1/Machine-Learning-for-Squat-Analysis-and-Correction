import imageio
import os

frames=[]

time=list(range(1, len(os.listdir('imgs'))))

for t in time:
    image = imageio.v2.imread(f'./imgs/img_{t}.png')
    frames.append(image)


imageio.mimsave('./gifs/example.gif', # output gif
                frames)