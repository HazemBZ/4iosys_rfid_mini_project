from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from raspi_app import clientlib
from raspi_app import app
import json
import requests

cl = None  # global client obj
app = Flask(__name__)
CORS(app)

## STATES
connected = {}

## COM DATA
advertisements = []
data_structs = []
IDs = set()  # save unique ids 

## CONFIG
SERVER_IP="192.168.1.10"


## CHANNELS
ADV_CHANNEL = "advertise"
COMMAND_ROOT = "command/" # work after concatinating the id sent by the esp
STATE_ROOT = "state/"     # the same 


## API endpoints
ADV_END_POINT = "http://127.0.0.1:5000/advertisements"

## Callback HELPER Functions

def handle_message(client, user_data, message):
  global IDs, STATE_ROOT
  dpayload = bytes.decode(message.payload, 'utf-8')
  # print("Topic: {0} | Payload: {1}".format(message.topic, dpayload))
  # if from 'advertisement' channel => save id
  # if from 'state' channel => associate the state with its ID
  if message.topic == ADV_CHANNEL:
    if dpayload not in IDs:
      IDs.add(dpayload)
      STATE_CHANNEL = STATE_ROOT + dpayload
      print("New advertised ID: {0} => Subscribing to Channel {1}".format(dpayload, STATE_CHANNEL))
      client.subscribe(STATE_CHANNEL)
  elif "state" in message.topic:
    id = message.topic.split('/')[1]
    print("ID: {0} REPORTED WITH STATE: {1}".format(id, dpayload))


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

cl = clientlib.connect(SERVER_IP , on_con=on_con, on_msg=on_msg )
print("connecting")
cl.loop_start()

## --------------------------

@app.route('/')
def home():
  global connected
  
  print(connected)
  messages = requests.get(ADV_END_POINT).json()
  return render_template("home.html", messages=messages)

## DATA STRUCTURE
# a message data structure has the following attributes: 'topic', 'payload', others
@app.route('/advertisements')
def messages_route():
  global data_structs
  messages = list(map(lambda x:{"topic":x["message"].topic, "payload":bytes.decode(x["message"].payload, "utf-8")}, data_structs))
  print(messages)
  return jsonify(messages)

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
  global cl, COMMAND_ROOT
  id = request.args.get('id')
  COMMAND_PATH = COMMAND_ROOT + id
  print("FROM: /command/open | COMMAND_PATH: %s".format(COMMAND_PATH))
  cl.publish(COMMAND_PATH, "OPEN")


  if __name__ == "__main__":
    print("in main")