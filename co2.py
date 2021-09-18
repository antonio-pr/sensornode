
import paho.mqtt.client as mqtt
import mh_z19
import json
from time import sleep
from getmac import get_mac_address as gma

freq = 5

def on_connect(client, userdata, flags, rc):
	print("Connected with result code"+str(rc))
	client.subscribe("/tfg/sensornode/data/change/" + gma())

def on_message(client, userdata, msg):
	global freq
	print(msg.topic+" "+str(msg.payload))
	data = json.loads(msg.payload.decode("utf-8"))
	freq = 60/ data["freq"]

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com",1883,60)
client.loop_start()


while(1):
	coef_co2 = mh_z19.read()
	client.publish("/tfg/sensornode/data/co2/" + gma(), json.dumps(coef_co2))
	sleep(freq)



