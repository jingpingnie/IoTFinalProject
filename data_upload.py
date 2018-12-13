import csv
from json import dumps
import requests
import numpy as np
import peakutils

# Define the file to upload
form = 'CPJ'
collection = 'trial'
trial = '1'
filename = 'AngleData_'+form+'_'+collection+trial+'.csv'

# Create 6 lists to store the angle data
arm_left_angle = []; arm_right_angle = []
elbow_left_angle = []; elbow_right_angle = []
knee_left_angle = []; knee_right_angle = []

ID = ['arm_left_angle', 'arm_right_angle', 'elbow_left_angle',
      'elbow_right_angle', 'knee_left_angle', 'knee_right_angle'];

# Read the Joint data from 'JointData.csv'

with open('C:\\Users\\Chen Liu (Raphael)\\Desktop\\Columbia Courses\\Fall 2018\\EECS E4764\\Final Project\\SkeletonBasics-D2D\\'+filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if ('nan' in (row[ID[0]])) or ('nan' in (row[ID[1]])) or ('nan' in (row[ID[2]])) or ('nan' in (row[ID[3]])) or ('nan' in (row[ID[4]])) or ('nan' in (row[ID[5]])):
            print('invalid row')
        else:
            arm_left_angle.append(row[ID[0]]); arm_right_angle.append(row[ID[1]]);
            elbow_left_angle.append(row[ID[2]]); elbow_right_angle.append(row[ID[3]]);
            knee_left_angle.append(row[ID[4]]); knee_right_angle.append(row[ID[5]]);

begin = 100
end = 1000
# Cut the data to the same size (500 data points per list)
arm_left_angle = arm_left_angle[begin:end]; arm_right_angle = arm_right_angle[begin:end]
elbow_left_angle = elbow_left_angle[begin:end]; elbow_right_angle = elbow_right_angle[begin:end]
knee_left_angle = knee_left_angle[begin:end]; knee_right_angle = knee_right_angle[begin:end]

# Convert the lists of strings to numpy arrays of floats.
a1 = np.array(list(map(float, arm_left_angle))); a2 = np.array(list(map(float, arm_right_angle)))
a3 = np.array(list(map(float, elbow_left_angle))); a4 = np.array(list(map(float, elbow_right_angle)))
a5 = np.array(list(map(float, knee_left_angle))); a6 = np.array(list(map(float, knee_right_angle)))

# Use transformed arrays to find the local minima and snip the data.
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

b1 = smooth(a1,8); b2 = smooth(a2,8)
b1 = -b1 + max(b1); b2 = -b2 + max(b2)
indice1 = peakutils.indexes(b1, thres=0.5/max(b1), min_dist=50)
indice2 = peakutils.indexes(b2, thres=0.5/max(b2), min_dist=50)

if len(indice1) < len(indice2):
    indice = indice1
else:
    indice = indice2

# Generate the 6 lists to upload. Each list will contain 10 sublists, where
# each sublist corresponds to 1 repetition.
a1_up = []; a2_up = []; a3_up = []; a4_up = []; a5_up = []; a5_up = []; a6_up = []

for index in range(10):
    low_idx = indice[index]
    high_idx = indice[index+1]
    sample_idx = np.arange(low_idx, high_idx, (high_idx-low_idx)/30)
    sample_idx = sample_idx.astype(int)
    if len(sample_idx) > 30:
        sample_idx = np.arange(low_idx, high_idx, (high_idx-low_idx)/29.8)
        sample_idx = sample_idx.astype(int)
    a1_up.append([arm_left_angle[i] for i in sample_idx])
    a2_up.append([arm_right_angle[i] for i in sample_idx])
    a3_up.append([elbow_left_angle[i] for i in sample_idx])
    a4_up.append([elbow_right_angle[i] for i in sample_idx])
    a5_up.append([knee_left_angle[i] for i in sample_idx])
    a6_up.append([knee_right_angle[i] for i in sample_idx])

# EC2 IP (public IP)
EC2_IP = 'http://3.16.31.183'

print('All invalid rows deleted.')

List = {'Form':form,
        'Trial':trial,
        'DataLength':len(arm_left_angle),
        'Data': {'arm_left_angle': a1_up,
                 'arm_right_angle': a2_up,
                 'elbow_left_angle': a3_up,
                 'elbow_right_angle': a4_up,
                 'knee_left_angle': a5_up,
                 'knee_right_angle': a6_up,
                 }
        }

for i in range(len(a1_up)):
    print(len(a1_up[i]))

# Upload the Joint Data
response = requests.post(EC2_IP, data = dumps(List))
print('Upload successful.')
