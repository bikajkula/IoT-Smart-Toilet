import paho.mqtt.client as mqtt

import firebase_admin

from firebase_admin import db

import time

import random

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


# Create a MQTT client
publisher = mqtt.Client()

# Connect to the MQTT broker
publisher.connect(broker_host, broker_port)

ref = db.reference("/toilet/seat/")

def simulate_temperature():
	# Simulate temperature within a range
	temperature = random.uniform(18, 30)
	return temperature

def post_temperature(temperature):

	print(f"Toilet seat temperature: {temperature} °C")

	# Save the temperature to Firebase Realtime Database
	ref.child('temperature').set(temperature)
	
# starting sim

temp = simulate_temperature()


post_temperature(temp)

while True:
	# Publish a message to a topic
	
	
	
	ref = db.reference("/toilet/seat/")
	
	temp = ref.child('temperature').get()
	
	publisher.publish("Kupatilo/solja/daska/temperatura", str(temp)+" °C")
	
	print(f"Toilet seat temperature: {temp} °C")
	
	time.sleep(5)

try:
    while True:
        pass
except KeyboardInterrupt:
    publisher.disconnect()
    publisher.loop_stop()
