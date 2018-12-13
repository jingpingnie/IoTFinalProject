# Open up the server to handle user data upload to mongodb.
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient()
db = client.final_project
posts = db.CPJ_userdata

IP = "172.31.36.126"
port = 80

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'You sent a GET request')

        def do_POST(self):
                global client, db, posts
                content_length = int(self.headers['Content-Length'])
                json_data = self.rfile.read(content_length)
                post_data = json.loads(json_data)
                self.send_response(200)
                self.end_headers()

                form = post_data['Form']#string
                trial = post_data['Trial']#string
                arm_left = post_data['Data']['arm_left_angle']
                arm_right = post_data['Data']['arm_right_angle']
                elbow_left = post_data['Data']['elbow_left_angle']
                elbow_right = post_data['Data']['elbow_right_angle']
                knee_left = post_data['Data']['knee_left_angle']
                knee_right = post_data['Data']['knee_right_angle']
                post = {'Trial':trial,'Arm_left':arm_left,'Arm_right':arm_right$
                mypost = posts.insert_one(post)
                print(mypost)

                response = BytesIO()
                response.write(b'This is a POST request. ')
                response.write(b'Received! ')
                response.write(b'Data uploaded: ')
                response.write(bytes(str(mypost), 'utf-8'))
                self.wfile.write(response.getvalue())

httpd = HTTPServer((IP, port), SimpleHTTPRequestHandler)
print('Starting httpd...')
httpd.serve_forever()
