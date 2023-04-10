import os

path_save='/home/mukundan/Desktop/VIII_SEM/Data/cam_recordings'

files=os.listdir(path_save)

for file in files:
	if not os.path.exists(os.path.join(os.path.join(path_save, file), 'label.txt')):
		with open(os.path.join(os.path.join(path_save, file), 'label.txt'), 'w') as label:
			label.write("powerlifting squats")


   