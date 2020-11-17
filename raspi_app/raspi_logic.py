from time import sleep
import paho.mqtt.client as mqtt

MQTT_SERVER = "192.168.1.7"
MQTT_PATH = "test_channel"

# when the client receives a CONNACK response form the server
def on_connect(client, userdata, flags, rc):
	print("Connect wirth result code "+str(rc))
	client.subscribe(MQTT_PATH) # if we lose the connection and reconnect the subscription will be renewed
	#while True:
	#	client.publish("esp/data", "hello esp")
	#	sleep(2)

# when PUBLISH msg is received from server
def on_message(client, userdata, msg):
	print(msg.topic + " " +str(msg.payload))

def on_publish(client, data, result):
	print("data published")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

#client.username_pw_set("dude", "dude")
client.connect(MQTT_SERVER, 1883)
ret = client.publish("esp/data", "hello esp")
print("message returnde ", ret)
#client.loop_forever() # if you do not want to write any more code
client.loop_start() # if you have more code to write
while True:
	client.publish("esp/data", "more data")
	sleep(1)
