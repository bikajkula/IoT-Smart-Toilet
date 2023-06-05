import paho.mqtt.client as mqtt

import firebase_admin

import random

import time


from firebase_admin import db


cred_object = firebase_admin.credentials.Certificate('cred.json ')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "dburl"
	})

address = ""	
ref = db.reference("/broker/")
ip = ref.get()

for k, v in ip.items():
	address = str(v)


broker_host = address  # Replace with the IP address or hostname of your MQTT broker
broker_port = 1883  # MQTT default port


#firestuff

ref = db.reference("/toilet/flush/")

l_press = list()


# Callback function for when a message is received
def on_message(client, userdata, message):
	
	last_press = False
	if len(l_press):
		last_press = l_press[-1] #get the last
	

	PRESSURED = message.payload.decode()
	l_press.append(PRESSURED) #add new one
	
	if last_press == "True" and PRESSURED == "False":  #someone just stood up
		ref.child('status').set(True)
		
		
		time.sleep(5)
		
		ref.child('status').set(False)
		
		
	
	
	#print(f"Received message: {message.payload.decode()} on topic '{message.topic}'")

# Create a MQTT client
subscriber = mqtt.Client()

# Set the callback function for message reception
subscriber.on_message = on_message

# Connect to the MQTT broker
subscriber.connect(broker_host, broker_port)

# Start the MQTT network loop to handle incoming/outgoing messages
subscriber.loop_start()

# Subscribe to a topic
subscriber.subscribe("Kupatilo/solja/daska/pritisak") 


# Keep the subscriber running
try:
    while True:
        pass
except KeyboardInterrupt:
    subscriber.disconnect()
    subscriber.loop_stop()
