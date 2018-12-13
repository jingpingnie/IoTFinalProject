#Train the IoT Final Project SVM (Posture)

from pymongo import MongoClient
from pprint import pprint
import json
import numpy as np
import imp
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib

# MongoDB collections
client = MongoClient()
db = client.final_project
form1 = db.CPJ_correct
form2 = db.CPJ_wrong0
form3 = db.CPJ_wrong1
form4 = db.CPJ_wrong2
form5 = db.CPJ_wrong3

# List for SVM

List = []
Label = ["correct"]*90 + ["wrong0"]*40 + ["wrong1"]*40 + ["wrong2"]*40

# CPJ_correct
for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
        x1 = np.array(form1.find_one({"Trial":i})["Arm_left"]).tolist()
        x2 = np.array(form1.find_one({"Trial":i})["Arm_right"]).tolist()
        x3 = np.array(form1.find_one({"Trial":i})["Elbow_left"]).tolist()
        x4 = np.array(form1.find_one({"Trial":i})["Elbow_right"]).tolist()
        x5 = np.array(form1.find_one({"Trial":i})["Knee_left"]).tolist()
        x6 = np.array(form1.find_one({"Trial":i})["Knee_right"]).tolist()
        for num in range(len(x1)):
                x = x1[num]+x2[num]+x3[num]+x4[num]+x5[num]+x6[num]
                List.append(x)

#CPJ_wrong0
for i in ['1', '2', '3', '4']:
        x1 = np.array(form2.find_one({"Trial":i})["Arm_left"]).tolist()
        x2 = np.array(form2.find_one({"Trial":i})["Arm_right"]).tolist()
        x3 = np.array(form2.find_one({"Trial":i})["Elbow_left"]).tolist()
        x4 = np.array(form2.find_one({"Trial":i})["Elbow_right"]).tolist()
        x5 = np.array(form2.find_one({"Trial":i})["Knee_left"]).tolist()
        x6 = np.array(form2.find_one({"Trial":i})["Knee_right"]).tolist()
        for num in range(len(x1)):
                x = x1[num]+x2[num]+x3[num]+x4[num]+x5[num]+x6[num]
                List.append(x)

#CPJ_wrong1
for i in ['1', '2', '3', '4']:
        x1 = np.array(form3.find_one({"Trial":i})["Arm_left"]).tolist()
        x2 = np.array(form3.find_one({"Trial":i})["Arm_right"]).tolist()
        x3 = np.array(form3.find_one({"Trial":i})["Elbow_left"]).tolist()
        x4 = np.array(form3.find_one({"Trial":i})["Elbow_right"]).tolist()
        x5 = np.array(form3.find_one({"Trial":i})["Knee_left"]).tolist()
        x6 = np.array(form3.find_one({"Trial":i})["Knee_right"]).tolist()
        for num in range(len(x1)):
                x = x1[num]+x2[num]+x3[num]+x4[num]+x5[num]+x6[num]
                List.append(x)

#CPJ_wrong2
for i in ['1', '2', '3', '4']:
        x1 = np.array(form4.find_one({"Trial":i})["Arm_left"]).tolist()
        x2 = np.array(form4.find_one({"Trial":i})["Arm_right"]).tolist()
        x3 = np.array(form4.find_one({"Trial":i})["Elbow_left"]).tolist()
        x4 = np.array(form4.find_one({"Trial":i})["Elbow_right"]).tolist()
        x5 = np.array(form4.find_one({"Trial":i})["Knee_left"]).tolist()
        x6 = np.array(form4.find_one({"Trial":i})["Knee_right"]).tolist()
        for num in range(len(x1)):
                x = x1[num]+x2[num]+x3[num]+x4[num]+x5[num]+x6[num]
                List.append(x)

# Train the SVM
lin_clf = svm.LinearSVC()
le = LabelEncoder
lin_clf.fit(List, Label)
joblib.dump(lin_clf, 'CL_angle_svm.pkl')
joblib.dump(le, 'CL_angle_svm_labelEncoder.pkl')
print(lin_clf)



