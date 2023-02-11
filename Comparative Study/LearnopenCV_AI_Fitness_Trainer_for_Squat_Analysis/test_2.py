# Python program to demonstrate
# creating a new file


# importing module
import os
import csv

# path of the current script
path_data='/home/mukundan/Desktop/VIII SEM/Data/Countix'
path_csv='/home/mukundan/Desktop/VIII SEM/Data/CSV_output'

# Before creating
dir_list = os.listdir(path_csv)
print("List of directories and files before creation:")
print(dir_list)
print()

# Creates a new file
field = ['Videoname', 'CameraAngled','Angle','Comments','CorrectCount','IncorrectCount','TotalCount']
rows = []
filename = "squat_data1.csv"
with open(os.path.join(path_csv, filename), 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(field)
    while True:
        Videoname = input("Videoname: ")
        CameraAngled = input("Camera Angled: ")
        Angle = input('OffsetAngle : ')
        Comments = input('Comments:')
        CorrectCount = int(input('CorrectCount: '))
        IncorrectCount= int(input('IncorrectCount: '))
        TotalCount = CorrectCount + IncorrectCount
        # writing the data rows
        csvwriter.writerow([Videoname, CameraAngled,Angle,Comments,CorrectCount,IncorrectCount,TotalCount])
        keep_going = input("Continue? [y/n]: ")
        if keep_going.lower() == "n":
            break


# After creating
dir_list = os.listdir(path_csv)
print("List of directories and files after creation:")
print(dir_list)
