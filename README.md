# IoT-Smart-Toilet

Mihajlo Karadžić
Filip Unčanin
Krsto Zarić

# O projektu
Projekat IoT Pametna WC šolja predstavlja sistem koji čini komunikacija u Discovery protokolu 
( prepoznavanje uređaja i, nama najbitnije, davanje osvežene IP adrese na kojoj je kontroler tj. broker ) 
i komunikacija u MQTT protokolu u vidu podataka koje objavljuju senzori i teme na koje se pretplaćuju aktuatori.
Najbitnije informacije se pamte na Firebase Realtime bazi podataka koje se koriste za simulaciju uređaja i upravljanju istih.
Kontrolni panel je realizovan u vidu GUI aplikacije u Pythonu preko koje je moguće kontrolisati najbitnije stavke WC šolje 
i gledanje podataka u realnom vremenu.

# O fajlovima

Za senzor pritiska:
	sensor1.py (Discovery) , sens_seat_pressure.py (MQTT)
	
Za senzor toplote daske:
	sensor2.py (Discovery), sens_seat_temperature.py (MQTT)

Za aktuator daske:
	act_seat_warmer.py (MQTT)

Za aktuator motora za pustanje vode:
	act_toilet_flusher.py (MQTT)
	
Za kontrolni panel:
	control_panel.py

# Potrebne biblioteke

- Pillow
- paho-mqtt
- netifaces
- firebase-admin
