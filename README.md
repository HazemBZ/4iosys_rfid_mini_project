## Setup
### Raspberry
#### mosquitto setup

**Installations**
```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
python3 -m pip install -r requirements.txt // cd to raspi_app first
```
#### Other setup

**Configuration**

/etc/mosquitto/mosquitto.conf
```
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d
#allow_anonymous false
#password_file /etc/mosquitto/pwfile
listener 1883
```

raspi_app/clientlib.py line 5
```
MQTT_SERVER = "127.0.0.1" // if running the web app on the pi
MQTT_SERVER = "raspberry_ip" // if not
```

raspi_app/app.py  line 21
```
SERVER_IP= "127.0.0.1" // if running the web app on the pi
SERVER_IP= "raspberry_ip" // if not
```

raspi_app/static/funs.js
```
WEB_APP_IP="127.0.0.1"  // localhost if the web app runs on the pi
WEB_APP_PORT="8884" // the port you are going to run the server on
```

esp8266_logic/esp8266_logic.ino
```
const char* ssid = "your_network_SSID"; // Broker server Network
const char* password = "your_network_password";  // Network pwd
const char* mqttServer ="the_rasberry_ip";  // Broker ip (raspi) 
```

**run wep app**
(from raspi_app)
```shell
FLASK_APP=app.py flask run --host 0.0.0.0 --port <portnumber>
```




