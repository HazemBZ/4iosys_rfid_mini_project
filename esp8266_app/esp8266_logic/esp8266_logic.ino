# include <ESP8266WiFi.h>
# include <PubSubClient.h>
#include <stdbool.h> 

bool eq = true;
const char* ssid = "problem_technique"; // Broker server Netwoek
const char* password = "esprit2020";  // Network pwd
const char* mqttServer ="192.168.1.11";  // Broker ip (raspi) 
const int mqttPort = 1883;  // default MQTT port 
const char* mqttUser = "";  // no credentials for now
const char* mqttPassword = "";  // no cred for now
const char* ID = "123"; // suppose this is a uid 
const char* STATE = "AOK"; // STATES: 'AOK' => all ok  | 'NOK' => not ok (maybe change to closed and open states)

// CHANNELS
const char* ADV_CHANNEL = "advertise";
const char* STATE_CHANNEL = "state/123";  //"state/" + ID;
const char* COMMAND_CHANNEL = "command/123";  //"command/" + ID;

// client
WiFiClient espClient;
PubSubClient client(espClient);






void setup() {  // START SETUP
  pinMode(2, OUTPUT);
  
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
  
  // CONNECT to mqtt server
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

  //client.publish(ADV_CHANNEL, "123"); // publish once your id (last ip adresse byte) "suppose this is a unique string"
  client.subscribe(COMMAND_CHANNEL); // listen for commands in this channel

} // --- END SETUP

  // HANDLE MESSAGES
  //// onMessage callback ( here filter and handle messages ) 
  void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived at topic: ");
    Serial.println(topic);

    // print message
    const char* str = "OPEN";
    
    Serial.print("Message:");
    for (int i=0; i<length; i++) { // fucking c shit comparison
      Serial.print((char)payload[i]);
      if ( (char)payload[i] != str[i]) { // checking for OPEN command
        // Serial.print("Equals");
        eq = false;
      }
      // strcat(str*, (char)payload[i]);
    }
    if (eq) {
      openLock();
    }
    Serial.print("In one conversion => ");
    // String str = (char*) payload;
    // char* str  = (char*)payload;
    Serial.println(str);
    Serial.println();
    Serial.print("----------");
  }


void ledOn() {
         // wait for a 0.5 second
}


// --- OPEN LOCK LOGIC HERE ---
void openLock(){
  Serial.print("ITS ON");       
  Serial.print("=>  LOCK OPENED  <=");
}

const int PUBLISH_INTERVAL = 2000;
void loop() { // keep publishing state at regular intervals
  client.loop();
  client.publish(ADV_CHANNEL, ID); // for now keep sending your ID
  // Serial.println("Published message TO ADV--");
  client.publish(STATE_CHANNEL, STATE); // keep sending state 
  delay(PUBLISH_INTERVAL);
   digitalWrite(2, HIGH);   // turn the LED on by making the pin 13 HIGH
  delay(1000);              // wait for a 0.5 second
  digitalWrite(2, LOW);    // turn the LED off by making the pin 13 LOW
  delay(1000);  
}
