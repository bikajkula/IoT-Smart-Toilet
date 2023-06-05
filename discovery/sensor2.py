import socket
import time
from pathlib import Path
import atexit
import sys
import json
import netifaces

from errno import ENETUNREACH

def get_local_non_loopback_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ipv4_addresses = addresses[netifaces.AF_INET]
            for address_info in ipv4_addresses:
                ip_address = address_info['addr']
                if not ip_address.startswith('127.'):
                    return ip_address
    return None

configId = "sensor2"

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

location = str(Path().absolute()) + "/" +str(configId) + ".json"

host_msg = "HOST: " + get_local_non_loopback_address() + " \n"


location_msg = "LOCATION: file://" + location + "\n"
cinfigid_msg = "CONFIGID.UPNP.ORG: " + configId + " \n"	
alive_msg = "NTS: ssdp:alive \n"
byebye_msg = "NTS: ssdp:byebye \n"

msg_2 = host_msg + location_msg + cinfigid_msg + byebye_msg

def exit_handler():
    sock.sendto(msg_2.encode(), (MCAST_GRP, MCAST_PORT))

atexit.register(exit_handler)
connected_temp = 0

while True:
	try:
		msg_1 = host_msg + location_msg + cinfigid_msg + alive_msg
		
		with open(location, 'r') as f:
			data = json.load(f)
		
		json_str = json.dumps(data)
	
		msg_1 += "JSON: " + json_str
		
		sock.sendto(msg_1.encode(), (MCAST_GRP, MCAST_PORT))
		
		if connected_temp == 0:
			connected_temp = 1
			print("Connected")
			
		time.sleep(3)
	except IOError:
		print("No connection. Retrying...")
		connected_temp = 0
		time.sleep(3)
	except:
		print("\nDisconnected")
		sys.exit(0)

