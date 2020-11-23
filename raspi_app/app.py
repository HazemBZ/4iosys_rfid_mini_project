from flask import Flask, render_template, jsonify
from flask_cors import CORS
from raspi_app import clientl
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

## CONFIG
SERVER_IP="192.168.1.6"


## CHANNELS
ADV_CHANNEL = "advertise"

## API endpoints
ADV_END_POINT = "http://127.0.0.1:5000/advertisements"

## HELPER Functions

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
  print("--MQTT message--")
  dir(message)



cl = clientl.connect(SERVER_IP , on_con=on_con, on_msg=on_msg )
print("connecting")
cl.loop_start()

@app.route('/')
def home():
  global connected
  
  print(connected)
  messages = requests.get(ADV_END_POINT).json()
  return render_template("home.html", messages=messages)

@app.route('/advertisements)
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

  if __name__ == "__main__":
    print("in main")