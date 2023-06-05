import tkinter as tk

import paho.mqtt.client as mqtt

import firebase_admin

from firebase_admin import db

import time


from PIL import ImageTk, Image


cred_object = firebase_admin.credentials.Certificate('cred.json ')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "dburl"
	})


ref = db.reference("/toilet/seat/")

ref1 = db.reference("/toilet/flush/")

warm = "0"

press = "0"

ref.child('warmer_status').set(False)

ref.child('pressured_status').set(False)

def button1_clicked():
	ref.child('warmer_status').set(True)
	label_text5.set("HEATER ON")		

def button2_clicked():
	ref.child('warmer_status').set(False)
	label_text5.set("HEATER OFF")

def button3_clicked():
	ref.child('pressured_status').set(True)
	label_text5.set("SEAT IS PRESSURED")
	
def button4_clicked():
	ref.child('pressured_status').set(False)
	label_text5.set("SEAT IS RELIEVED")

def display_image(image_path):
	image = Image.open(image_path)
	photo = ImageTk.PhotoImage(image)
	label.configure(image=photo)
	label.image = photo  # Keep a reference to prevent garbage collection

def update_temp():
	temperature = ref.child('temperature').get()
	
	pressured = ref.child('pressured_status').get()
	
	flush_status = ref1.child('status').get()

	

	
	if temperature > 25:
		warm = "1"
	else:
		warm = "0"
	
	if pressured:
		press = "1"
	else:
		press = "0"
	
	label_text.set(str(round(temperature, 1))+"  °C")
	
	
	if flush_status:
		label_text5.set("FLUSHING...")
		display_image("flushing.gif")
		
		window.after(1000, update_temp)
		
	else:
		label_text5.set("IDLE...")
		display_image(warm+press+".jpg")
	
		window.after(3000, update_temp)
	
def update_heat():
	warmer = ref.child('warmer_status').get()

	label_text3.set(str(warmer))
	
	window.after(4500, update_heat)
	

# Create the main window
window = tk.Tk()
window.title("GUI App")

# Create a frame to hold the picture
picture_frame = tk.Frame(window)
picture_frame.pack(side=tk.RIGHT)

# Load and display the initial image in the frame
initial_image = Image.open("default.png")
photo = ImageTk.PhotoImage(initial_image)
label = tk.Label(picture_frame, image=photo)
label.pack()

# Create the buttons
button1 = tk.Button(window, text="Heater ON", command=button1_clicked)
button1.pack()

button2 = tk.Button(window, text="Heater OFF", command=button2_clicked)
button2.pack()

button3 = tk.Button(window, text="Sit down", command=button3_clicked)
button3.pack()

button4 = tk.Button(window, text="Get up", command=button4_clicked)
button4.pack()

# Create a label
label_text1 = tk.StringVar()
label_text1.set("\nTemperature:")
text_label1 = tk.Label(window, textvariable=label_text1)
text_label1.pack()

# Create a label
label_text = tk.StringVar()
label_text.set("Initial text")
text_label = tk.Label(window, textvariable=label_text)
text_label.pack()

# Create a label
label_text2 = tk.StringVar()
label_text2.set("\nSeat warmer is on:")
text_label2 = tk.Label(window, textvariable=label_text2)
text_label2.pack()

# Create a label
label_text3 = tk.StringVar()
label_text3.set("Initial text")
text_label3 = tk.Label(window, textvariable=label_text3)
text_label3.pack()


# Create a label
label_text4 = tk.StringVar()
label_text4.set("\nStatus:")
text_label4 = tk.Label(window, textvariable=label_text4)
text_label4.pack()

# Create a label
label_text5 = tk.StringVar()
label_text5.set("STATUS")
text_label5 = tk.Label(window, textvariable=label_text5)
text_label5.pack()

update_temp()

update_heat()

# Start the main loop
window.mainloop()

