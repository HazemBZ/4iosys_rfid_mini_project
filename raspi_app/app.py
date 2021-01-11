from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from raspi_app import clientlib
from raspi_app import app
import json
import requests

from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading

PORT="8884"

#def flask_wrapper():
cl = None  # global client obj
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

## STATES
connected = {}
OPENED = False

## COM DATA
advertisements = []
data_structs = []
IDs = set()  # save unique ids 
states = {} # s

## CONFIG
MQTT_SERVER_IP="192.168.1.8"
WEB_APP_SERVER_IP="192.168.1.8"
PORT="8884"


## CHANNELS
ADV_CHANNEL = "advertise"
COMMAND_ROOT = "command/" # work after concatinating the id sent by the esp
STATE_ROOT = "state/"     # the same 


## API endpoints
ADV_END_POINT = "http://{ip}:{port}/advertisements".format(port=PORT, ip=WEB_APP_SERVER_IP)


## Callback HELPER Functions

def log_message(message):
  global advertisements
  advertisements.append(message)

def handle_message(client, user_data, message):
	global IDs, STATE_ROOT, states
	dpayload = bytes.decode(message.payload, 'utf-8')
	# print("Topic: {0} | Payload: {1}".format(message.topic, dpayload))
	# if from 'advertisement' channel => save id
	# if from 'state' channel => associate the state with its ID
	log_message({"topic":message.topic, "payload":dpayload})
	if message.topic == ADV_CHANNEL:
		if dpayload not in IDs:
			IDs.add(dpayload)
			STATE_CHANNEL = STATE_ROOT + dpayload
			print("New advertised ID: {0} => Subscribing to Channel {1}".format(dpayload, STATE_CHANNEL))
			client.subscribe(STATE_CHANNEL)
	elif "state" in message.topic:
		id = message.topic.split('/')[1]
		print("ID: {0} REPORTED WITH STATE: {1}".format(id, dpayload))
		states.update({id: dpayload})


def on_con(client, user_data, flags, rc):
	global connected, cl
	connected = {"user_data":user_data, "flags":flags, "rc":rc}
	print("on_connected")
	# print(connected)
	client.subscribe(ADV_CHANNEL)
	# cl = client

def on_msg(client, user_data, message): ## filter messages here 
	global q_messages
	data_structs.append({"client":client, "user_data":user_data, "message":message})
	# print("--MQTT message--")
	# print(dir(message))
	handle_message(client, user_data, message)

## -------- CLIENT ---------
# cl is the mqtt client agent 

cl = clientlib.connect(MQTT_SERVER_IP , on_con=on_con, on_msg=on_msg )
print("connecting")
cl.loop_start()

  ## --------------------------

  # @app.after_request
  # def add_header(r):
  #     """
  #     Add headers to both force latest IE rendering engine or Chrome Frame,
  #     and also to cache the rendered page for 10 minutes.
  #     """
  #     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  #     r.headers["Pragma"] = "no-cache"
  #     r.headers["Expires"] = "0"
  #     r.headers['Cache-Control'] = 'public, max-age=0'
  #     return r


<<<<<<< HEAD
  @app.route('/')
  def home():
    #global connected, advertisements, states
    
    print(connected)
    print("")
    # messages = requests.get(ADV_END_POINT).json()
    return render_template("home.html", messages=advertisements, states=list(states.items()))

  ## DATA STRUCTURE
  # a message data structure has the following attributes: 'topic', 'payload', others
  @app.route('/advertisements')
  def messages_route():
    #global data_structs, advertisements
    # messages = list(map(lambda x:{"topic":x["message"].topic, "payload":bytes.decode(x["message"].payload, "utf-8")}, data_structs))
    print("GET /advertisements ", advertisements)
    return jsonify(advertisements)

  @app.route('/advertisement/<id>')
  def one_message(id):
    #global data_structs
    print(data_structs[int(id)-1]["message"])
    message = data_structs[int(id)-1]["message"]
    #print(dir(message))
    return jsonify({"topic": message.topic, "payload":bytes.decode(message.payload, "utf-8")})


  # COMMAND API
  ## Commands to implement: open, close

  @app.route('/command/open')
  def open_command():
    #global cl, COMMAND_ROOT
    id = request.args.get('id')
    COMMAND_PATH = COMMAND_ROOT + id
    print("FROM: /command/open | COMMAND_PATH: %s".format(COMMAND_PATH))
    cl.publish(COMMAND_PATH, "OPEN")
    return jsonify(states.get(id))

  ## closing has to be manual
=======
@app.route('/')
def home():
	global connected, advertisements, states

	print(connected)
	print("")
	# messages = requests.get(ADV_END_POINT).json()
	return render_template("home.html", messages=advertisements, states=list(states.items()))

## DATA STRUCTURE
# a message data structure has the following attributes: 'topic', 'payload', others
@app.route('/advertisements')
def messages_route():
	global data_structs, advertisements
	# messages = list(map(lambda x:{"topic":x["message"].topic, "payload":bytes.decode(x["message"].payload, "utf-8")}, data_structs))
	print("GET /advertisements ", advertisements)
	return jsonify(advertisements)

@app.route('/advertisement/<id>')
def one_message(id):
	global data_structs
	print(data_structs[int(id)-1]["message"])
	message = data_structs[int(id)-1]["message"]
	#print(dir(message))
	return jsonify({"topic": message.topic, "payload":bytes.decode(message.payload, "utf-8")})


# COMMAND API
## Commands to implement: open, close

@app.route('/command/open')
def open_command():
	global cl, COMMAND_ROOT, OPENED
	if(not OPENED):
		id = request.args.get('id')
		COMMAND_PATH = COMMAND_ROOT + id
		print("FROM: /command/open | COMMAND_PATH: %s".format(COMMAND_PATH))
		cl.publish(COMMAND_PATH, "OPEN")
		OPENED = True
	return jsonify(states)#jsonify(states.get(id))

@app.route('/command/close')
def close_command():
        global cl, COMMAND_ROOT, OPENED
        if(OPENED):
                id = request.args.get('id')
                COMMAND_PATH = COMMAND_ROOT + id
                print("FROM: /command/close | COMMAND_PATH: %s".format(COMMAND_PATH))
                cl.publish(COMMAND_PATH, "CLOSE")
                OPENED = False
        return jsonify(states)


## closing has to be manual
>>>>>>> be3179349f3146c26f64e2c1080fb5bf957fe830

def rfid_wrapper():
  reader = SimpleMFRC522()
  while True:
    try:
      id, text = reader.read()
      print("id: {0}; text: {1}".format(id, text))
      requests.get("localhost:{0}/command/open?id=123".format(PORT))
    except Exception as e:
      print(e.message())
    finally:
      GPIO.cleanup()
      sleep(3)


if __name__ == "__main__":
  print("in main")
#t1 = threading.Thread(target=flask_wrapper)
#t2 = threading.Thread(target=rfid_wrapper)

#t1.start()
#t2.start()

#t1.join()
#t2.join()
