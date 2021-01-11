from time import sleep
import paho.mqtt.client as mqtt


MQTT_SERVER = "192.168.1.8"	# Change it to the IP of the broker server you are using (eg: Mosquitto)
MQTT_PORT = 1883	# default port
ADV_PATH = "advertise"	# channel to which locker MCU will advertise their presence

client = None
# when the client receives a CONNACK response form the server
def on_connect(client, userdata, flags, rc):
	print("Connect wirth result code "+str(rc))
	client.subscribe(ADV_PATH) # if we lose the connection and reconnect the subscription will be renewed
															# subscribe to esp32 
	#while True:
	#	client.publish("esp/data", "hello esp")
	#	sleep(2)

# when PUBLISH msg is received from server
def on_message(client, userdata, msg):
	print(msg.topic + " " +str(msg.payload))

def on_publish(client, data, result):
	print("data published")

def connect(mqtt_server=MQTT_SERVER, mqtt_port=MQTT_PORT, on_con=None, on_msg=None, on_pub=None):
	global client
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_publish = on_publish
	if on_msg:
		client.on_message = on_msg
	if on_con:
		client.on_connect = on_con
	if on_pub:
		client.on_publish= on_pub
	client.connect(mqtt_server, mqtt_port)
	return client


#client.username_pw_set("dude", "dude")

# ret = client.publish("esp/data", "hello esp")
# print("message returnde ", ret)

#client.loop_forever() # if you do not want to write any more code

# client.loop_start() # if you have more code to write

# while True:
# 	client.publish("esp/data", "more data")
# 	sleep(1)
