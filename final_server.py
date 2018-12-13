# IoT Lab6 SVM Application
# This is the EC2 server
# Predict the character correponding to the data sent from ESP8266

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from pymongo import MongoClient
from pprint import pprint
import json
import numpy as np
import imp
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
import requests
from decimal import Decimal

client = MongoClient()
db_intensity = client.Lab6_check1_database
db_posture = client.final_project
form = db_posture.CPJ_userdata

#posts_C = db_intensity.TrainingC 

IP = "172.31.36.126"
port = 80

# Workout Intensity Classification
our_clf = joblib.load('final_svm_model.pkl')
our_le = joblib.load('final_svm_labelEncoder.pkl')
prediction = []

# Posture Correctness Classfication
posture_clf = joblib.load('CL_angle_svm.pkl')
posture_le = joblib.load('CL_angle_svm_labelEncoder.pkl')

m = 0

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'You sent a GET request')

	def do_POST(self):
		global client, db_intensity, posts, m
		content_length = int(self.headers['Content-Length'])
		json_data = self.rfile.read(content_length)
		post_data = json.loads(json_data)
		self.send_response(200)
		self.end_headers()

		character = post_data['Character']

		if character == "first":
			
			tweet_to_post = post_data['Count']
			print(tweet_to_post)
			ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/CCR.mp4"
			print(ThingSpeak_API_URL)

	
			response = BytesIO()
			response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
			self.wfile.write(response.getvalue())

		elif character == "second":
			
			tweet_to_post = post_data['Count']
			print(tweet_to_post)
			ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/CMD.mp4"#https://cloud.video.taobao.com/play/u/651477717/p/1/e/6/t/1/50008268107.mp4"
			print(ThingSpeak_API_URL)
			
	
			response = BytesIO()
			response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
			self.wfile.write(response.getvalue())

		elif character == "Third":
			
			tweet_to_post = post_data['Count']
			print(tweet_to_post)
			ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/CPJ.mp4"#https://cloud.video.taobao.com/play/u/651477717/p/1/e/6/t/1/50008268107.mp4"
			print(ThingSpeak_API_URL)
			
	
			response = BytesIO()
			response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
			self.wfile.write(response.getvalue())

		elif character == "for":
			
			tweet_to_post = post_data['Count']
			print(tweet_to_post)
			ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/ZMD.mp4"#https://cloud.video.taobao.com/play/u/651477717/p/1/e/6/t/1/50008268107.mp4"
			print(ThingSpeak_API_URL)
			
	
			response = BytesIO()
			response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
			self.wfile.write(response.getvalue())

		elif character == "five":
			
			tweet_to_post = post_data['Count']
			print(tweet_to_post)
			ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/ZMJ.mp4"#https://cloud.video.taobao.com/play/u/651477717/p/1/e/6/t/1/50008268107.mp4"
			print(ThingSpeak_API_URL)
			
	
			response = BytesIO()
			response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
			self.wfile.write(response.getvalue())

		elif character == "classification":
			print('Classification')
			posture_prediction = []

			# Use the IoT final project SVM classfication data
			x1 = np.array(form.find_one({"Trial":'1'})["Arm_left"]).tolist()
			x2 = np.array(form.find_one({"Trial":'1'})["Arm_right"]).tolist()
			x3 = np.array(form.find_one({"Trial":'1'})["Elbow_left"]).tolist()
			x4 = np.array(form.find_one({"Trial":'1'})["Elbow_right"]).tolist()
			x5 = np.array(form.find_one({"Trial":'1'})["Knee_left"]).tolist()
			x6 = np.array(form.find_one({"Trial":'1'})["Knee_right"]).tolist()
			for num in range(10):
				x = x1[num] + x2[num] + x3[num] + x4[num] + x5[num] + x6[num]
				posture_prediction.append(posture_clf.predict([np.asarray(x).astype(np.float64)]))
			num_correct = 0; num_wrong0 = 0; num_wrong1 = 0; num_wrong2 = 0;
			print(len(posture_prediction))
			for num in range(len(posture_prediction)):
				if posture_prediction[num] == ["correct"]:
					num_correct += 1
				elif posture_prediction[num] == ["wrong0"]:
					num_wrong0 += 1
				elif posture_prediction[num] == ["wrong1"]:
					num_wrong1 += 1
				elif posture_prediction[num] == ["wrong2"]:
					num_wrong2 += 1
			print(num_correct)

			if max(num_correct,num_wrong0,num_wrong1,num_wrong2) == num_wrong0:
				tweet_to_post = post_data['Count']
				print(tweet_to_post)
				ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/wrong0.mp4"
				print(ThingSpeak_API_URL)
				response = BytesIO()
				response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
				self.wfile.write(response.getvalue())

			elif max(num_correct,num_wrong0,num_wrong1,num_wrong2) == num_wrong1:
				tweet_to_post = post_data['Count']
				print(tweet_to_post)
				ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/wrong1.mp4"
				print(ThingSpeak_API_URL)				
				response = BytesIO()
				response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
				self.wfile.write(response.getvalue())
		
			elif max(num_correct,num_wrong0,num_wrong1,num_wrong2) == num_wrong2:
				tweet_to_post = post_data['Count']
				print(tweet_to_post)
				ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/wrong2.mp4"
				print(ThingSpeak_API_URL)
				response = BytesIO()
				response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
				self.wfile.write(response.getvalue())
		
			elif max(num_correct,num_wrong0,num_wrong1,num_wrong2) == num_correct:
				tweet_to_post = post_data['Count']
				print(tweet_to_post)
				ThingSpeak_API_URL = "https://raw.githubusercontent.com/jingpingnie/IoTFinalProject/master/correct.mp4"
				print(ThingSpeak_API_URL)				
				response = BytesIO()
				response.write(bytes(str(ThingSpeak_API_URL), 'utf-8'))
				self.wfile.write(response.getvalue())
		
		else:

			# Extract the acceleration in x and y directions.
			acc_x = post_data['Data']['Data_x']
			acc_y = post_data['Data']['Data_y']
			acc_z = post_data['Data']['Data_z']

			# Convert them to the correct format: [[x1, x2 ...], [y1, y2 ...]]
			x = np.array(acc_x).tolist()
			y = np.array(acc_y).tolist()
			z = np.array(acc_z).tolist()
			#x = np.array(posts_C.find_one({"count":19})["acc_x"]).tolist()
			#y = np.array(posts_C.find_one({"count":19})["acc_y"]).tolist()
			xy = x+y+z

			# Predict the charactekr
			pred = our_clf.predict([np.asarray(xy).astype(np.float64)])
			prediction.append(our_clf.predict([np.asarray(xy).astype(np.float64)]))
			print(prediction)
			
			if pred == 'M':
				m+=1


			ratio = round(Decimal(m/len(prediction)),4)

			print(ratio)


			# Send the response
			response = BytesIO()
			#response.write(b'This is a POST request. ')
			#response.write(b'Data received.')
			#response.write(b'Predicted character: ')
			response.write(bytes(str(ratio), 'utf-8'))
			self.wfile.write(response.getvalue())


httpd = HTTPServer((IP, port), SimpleHTTPRequestHandler)
print('Starting httpd...')
httpd.serve_forever()
