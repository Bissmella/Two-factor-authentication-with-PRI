import cv2
import face_recognition
import serial
import pymongo
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import time

#function to turn on red LED (login failure)
def led_red():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(13,GPIO.OUT)
	for i in range(5):
		GPIO.output(13, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(13, GPIO.LOW)
		time.sleep(1)
#function to turn on green LED (login success)
def led_green():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(11,GPIO.OUT)
	for i in range(5):
		GPIO.output(11, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(11, GPIO.LOW)
		time.sleep(1)

#setting mqtt and message sending function
client = mqtt.Client()
def senddata(data, state):
	client.connect('YOUR-MQTT-BROKER', 'YOUR-MQTT-BROKER-PORT')
	client.subscribe('YOUR-TOPIC', qos=0)
	print('\n sending data')
	d = {"ID": data, "attempt": state}
	djson = json.dumps(d)
	client.publish('YOUR-TOPIC', djson)
	client.disconnect()


#setting mongodb database connection
myclient = pymongo.MongoClient("YOUR MONGODB ADDRESS")
db = myclient["DB-NAME"]
user_col = db["users"]
#setting rfid card reader
PortRF = serial.Serial('/dev/ttyAMA0', 9600)
while True:
	print ('\n please scan your card')
	ID= ""
	read_byte = PortRF.read(12)
	print ("rawData:",read_byte)
	if read_byte[0] == 2 : 	#reading rfid card
		for Counter in range (1, 12):
			ID = ID + chr (read_byte[Counter])
		print ('\n ID:' + str(ID))
	if user_col.count_documents({'ID': str(ID)}) > 0: #checking if the user is registered with database
		img = cv2.imread('dataset/'+str(ID)+'.jpg')   #Loading user's original image
		rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting user's image from BGR to RGB
		img_encoding = face_recognition.face_encodings(rgb_img)[0] #encoding the face in image
		#Setting the camera for photo capture
		cam = cv2.VideoCapture(0)
		cam.set(3, 640)
		cam.set(4, 480)
		count = 0
		while count<1: 		#Getting image until a face is detected
			ret, imag2 = cam.read()
			img2 = cv2.flip(imag2, -1)
			rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
			img_encoding2 = face_recognition.face_encodings(rgb_img2)
			if len(img_encoding2)>0: #checing if face detected in caputred image
				count +=1
			else:
				print("\n please keep appropriate distance from camera!!")
		cam.release()
		cv2.destroyAllWindows()
		#comparing the original face of the user with the captured face image
		result = face_recognition.compare_faces([img_encoding], img_encoding2[0], tolerance=0.4)
		print("Result: ", result)
		#turning on red or green lights based on the result and sending data to rpi2 through mqtt
		if result[0]:
			senddata(ID, "True")
			led_green()
		else:
			senddata(ID, "False")
			led_red()
	else:
		print ('\n you are not registered')



		
		
