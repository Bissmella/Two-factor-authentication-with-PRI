import cv2
import face_recognition
import serial
#import base64
from PIL import Image
import pymongo
import io

#setting the camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
#setting mqtt and mongodb database connections
myclient = pymongo.MongoClient("etu-web2.ut-capitole.fr")
db = myclient["bis_alij"]
user_col = db["users"]
#setting rfid scanner
PortRF = serial.Serial('/dev/ttyAMA0', 9600)
while True:
	#scanning RFID card
	print ('\n  please scan the card')
	ID= ""
	read_byte = PortRF.read(12)
	print ("rawData:",read_byte)
	if read_byte[0] == 2 :
		for Counter in range (1,12):
			ID = ID + chr(read_byte[Counter])
	#checking if card was not already registered in mongodb database
	if user_col.count_documents({'ID':  str(ID)}) == 0:
		#getting user details
		print ('\n ID: ' + str(ID))
		firstName = input('\n Enter first name ==> ')
		lastName = input('\n Enter last name ==>')
		#taking face picture
		print("\n Initializing face capture. look the camera and wait ...")
		if cam.isOpened():
			current_frame = 0
			while current_frame < 1:
				print('\n Please look at the camera')
				ret, imag = cam.read()
				if ret:
					img = cv2.flip(imag, -1)
					rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting image from BGR to RGB
					img_encoding = face_recognition.face_encodings(rgb_img) #encoding face in the image
					print('\n picture taken, detecting face')
					if len(img_encoding)>0:		#checking if any face was detected
						print('\n face detected')
						cv2.imwrite("dataset/" + str(ID) + ".jpg", img)		#writing image to file
						current_frame +=1
						#saving the captured image to database
						im = Image.open("dataset/"+str(ID) +".jpg")
						img_bytes = io.BytesIO()
						im.save(img_bytes, format = 'JPEG')
						data_dict = {'ID': str(ID), 'firstName': str(firstName), 'lastName': str(lastName), 'image': img_bytes.getvalue()}
						x = user_col.insert_one(data_dict)
	else:
		print('\n card already registered')
	#clean up and exiti program
	print("\n Exiting program and cleaning up")
	cam.release()
	cv2.destroyAllWindows()
	cv2.destroyAllWindows()
