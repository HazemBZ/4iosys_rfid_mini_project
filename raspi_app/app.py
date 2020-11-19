from flask import Flask, render_template, jsonify
from flask_cors import CORS
from raspi_app import clientl
from raspi_app import app
import json
import requests

cl = None
app = Flask(__name__)
CORS(app)
data_structs = []
connected = {}
MESSAGES_END_POINT = "http://127.0.0.1:5000/messages"

## helpers

def on_con(client, user_data, flags, rc):
  global connected, cl
  connected = {"user_data":user_data, "flags":flags, "rc":rc}
  print("on_connected")
  # print(connected)
  client.subscribe("test_channel")
  # cl = client

def on_msg(client, user_data, message):
  global q_messages
  data_structs.append({"user_data":user_data, "message":message})



cl = clientl.connect("192.168.1.6" , on_con=on_con, on_msg=on_msg )
print("connecting")
cl.loop_start()

@app.route('/')
def home():
  global connected
  
  print(connected)
  messages = requests.get(MESSAGES_END_POINT).json()
  return render_template("home.html", messages=messages)

@app.route('/messages')
def messages_route():
  global data_structs
  messages = list(map(lambda x:{"topic":x["message"].topic, "payload":bytes.decode(x["message"].payload, "utf-8")}, data_structs))
  print(messages)
  return jsonify(messages)

@app.route('/message/<id>')
def one_message(id):
  global data_structs
  print(data_structs[int(id)-1]["message"])
  message = data_structs[int(id)-1]["message"]
  #print(dir(message))
  return jsonify({"topic": message.topic, "payload":bytes.decode(message.payload, "utf-8")})

  if __name__ == "__main__":
    print("in main")