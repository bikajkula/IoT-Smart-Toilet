import paho.mqtt.client as mqtt

import firebase_admin

import random

from firebase_admin import db

import time

cred_object = firebase_admin.credentials.Certificate('cred.json ')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "dburl"
	})


ref = db.reference("/toilet/seat/")

def simulate_temperature():
	# Simulate temperature within a range
	temperature = random.uniform(18, 30)
	return temperature
	
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

def get_pressured_status():
	# Retrieve the seat pressured status from Firebase
	pressured_status = ref.child('pressured_status').get()
	return pressured_status

def post_temperature(temperature):

	print(f"Toilet seat temperature: {temperature} °C")

	# Save the temperature to Firebase Realtime Database
	ref.child('temperature').set(temperature)

def simulate_toilet_seat():
	temperature = temp
	while True:
		temperature = simulate_temperature_with_reference(temperature)
		warmer_status = get_warmer_status()
		pressured_status = get_pressured_status()
		
		# Increase temperature if the heater is on
		if temperature < 30: # 30 C is a limit for our heater
			if warmer_status:
				temperature += random.uniform(1, 3)
		else:
		# Decrease temp if the heater is turned off and no one is sitting 
		
			if not warmer_status:
				if not pressured_status:
					temperature -= random.uniform(7, 10)
					
		

		post_temperature(temperature)
		time.sleep(5)  # Simulate temperature every 5 seconds

simulate_toilet_seat()
