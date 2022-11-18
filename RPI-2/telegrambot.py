import time
import datetime
import paho.mqtt.client as mqtt
import telegram
import pymongo
import json

#setting up mqtt and mongodb connection
myclient = pymongo.MongoClient("YOUR MONGODB ADDRESS")
db = myclient["DB-NAME"]
#logs collection in mongodb database
log_col = db["logs"]
api_key = '5610830737:AAFLlS30ZsJ3bvIuqHqcyykqqY2NWsby0Xg'
user_id = '746524823'
#collection for telegram subscribers
bot_col = db["telegram"]
teles = bot_col.find()
#function to be called when a message is received through mqtt
def on_message(client, data, message):
	print ("Received: " + str(message.payload))
	bot = telegram.Bot(token=api_key)
	m_decode=str(message.payload.decode("utf-8","ignore"))
	#decode json message
	m_in=json.loads(m_decode) 
	timenow = datetime.datetime.now().isoformat() #getting current time for log
	#sending message for telegram subscribers to inform them of log in attempt
	if str(m_in["attempt"]) == "True":
		for tel in teles:
			print ('\n tele: ' + str(tel["chatid"]))
			try:
				bot.send_message(chat_id=tel["chatid"], text="user with id "+str(m_in["ID"])+" was logged in " + str(timenow) )
			except:
				pass
	else:
		for tel in teles:
			print ('\n tele: ' + str(tel["chatid"]))
			try:
				bot.send_message(chat_id=tel["chatid"], text="user with id "+str(m_in["ID"])+" tried to log in at " + str(timenow) )
			except:
				pass
	#storing event in database
	data_dict = {'ID': str(m_in["ID"]), 'datetime': timenow, 'attempt': m_in['attempt']}
	x = log_col.insert_one(data_dict)

#setting mqtt connection
client = mqtt.Client()
client.connect('YOUR MQTT BORKER ADDRESS', 'MQTT BROKER PORT')
client.on_message = on_message
client.subscribe('YOUR-TOPIC', qos=0)
client.loop_forever()

