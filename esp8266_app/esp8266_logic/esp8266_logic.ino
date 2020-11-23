# include <ESP8266WiFi.h>
# include <PubSubClient.h>

const char* ssid = "PLANET_007"; // Broker server Netwoek
const char* password = "hamatari";  // Network pwd
const char* mqttServer ="192.168.1.10";  // Broker ip (raspi) 
const int mqttPort = 1883;  // default MQTT port 
const char* mqttUser = "";  // no credentials for now
const char* mqttPassword = "";  // no cred for now
const char* ID = "123"; // suppose this is a uid 
const char* STATE = "I AM OK!->state"; // STATE struct mockup

// CHANNELS
const char* ADV_CHANNEL = "advertisement";
const char* STATE_CHANNEL = "state/" + ID;
const char* COMMAND_CHANNEL = "command/" + ID;

// client
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {  // START SETUP
  Serial.begin(9600);
  // wifi connection 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to Wifi ...");
  }
  Serial.println("Connected to Wifi network");

  // set server
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  
  // connect to mqtt server
  while(!client.connected()) { // Keep trying to connect
    Serial.println("Connecting to MQTT ...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed to connect with state");
      Serial.print(client.state());
      delay(2000);
    }
  }
  const id
  //client.publish(ADV_CHANNEL, "123"); // publish once your id (last ip adresse byte) "suppose this is a unique string"
  client.subscribe(COMMAND_CHANNEL); // listen for commands in this channel

} // --- END SETUP

  // onMessage callback ( here filter and handle messages ) 
  void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived at topic: ");
    Serial.println(topic);

    // print message
    Serial.print("Message:");
    for (int i=0; i<length; i++) {
      Serial.print((char)payload[i]);
    }
    Serial.println();
    Serial.print("----------");
  }

void loop() { // keep publishing state at regular intervals
  client.loop();
  client.publish(ADV_CHANNEL, ID); // for now keep sending ID
  client.publish(STATE_CHANNEL, STATE);
  delay(2000);
}
