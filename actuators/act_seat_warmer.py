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

ref = db.reference("/toilet/seat/")

l_temp = list()

l_press = list()

def simulate_temperature_with_reference(temp):
	# Simulate temperature within a range
	
	temp_1 = int(temp) - 1
	temp_2 = int(temp) + 1
	temperature = random.uniform(temp_1, temp_2)
	
	while temperature < 18:
		temperature = random.uniform(temp_1, temp_2)
	
	return temperature

def get_warmer_status():
	# Retrieve the warmer status from Firebase
	warmer_status = ref.child('warmer_status').get()
	return warmer_status


def post_temperature(temperature):

	print(f"Toilet seat temperature: {temperature} °C")

	# Save the temperature to Firebase Realtime Database
	ref.child('temperature').set(temperature)

def simulate_toilet_seat(t,p):
	temperature = t
	
	press = p
	
	pressured_status = True


	if press == "True":
		pressured_status = True
	else:
		pressured_status = False

	
	temperature = simulate_temperature_with_reference(temperature)
	warmer_status = get_warmer_status()
	
	# Increase temperature if the heater is on
	if temperature < 30:	# 30 C is the limit for our heater
		if warmer_status:  
			temperature += random.uniform(1, 3)
	else:
	# Decrease temp if the heater is turned off and no one is sitting 
		if not warmer_status:
			if not pressured_status or temperature > 35:
				temperature -= random.uniform(7, 12)
		else:
			temperature = 30 + random.uniform(0, 1)
	

	post_temperature(temperature)




##


# Callback function for when a message is received
def on_message(client, userdata, message):
	if message.topic == "Kupatilo/solja/daska/temperatura":
		TEMP = message.payload.decode()
		TEMP = TEMP.split()
		TEMP = float(TEMP[0])
		l_temp.insert(0,TEMP)
	elif message.topic == "Kupatilo/solja/daska/pritisak":
		PRESSURED = message.payload.decode()
		l_press.insert(0,PRESSURED)
	
	if len(l_temp) and len(l_press):
		simulate_toilet_seat(l_temp[0],l_press[0])
		
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
subscriber.subscribe("Kupatilo/solja/daska/temperatura")

subscriber.subscribe("Kupatilo/solja/daska/pritisak") 


# Keep the subscriber running
try:
    while True:
        pass
except KeyboardInterrupt:
    subscriber.disconnect()
    subscriber.loop_stop()
