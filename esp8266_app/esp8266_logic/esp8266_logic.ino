# include <ESP8266WiFi.h>
# include <PubSubClient.h>
#include <stdbool.h> 
#include "Servo.h"


//bool eq = true;
//bool c_eq = true;
bool open_the_lock = false;
bool close_the_lock = false;
const char* ssid = "your_ssid"; // Broker server Netwoek
const char* password = "your_pass";  // Network pwd
const char* mqttServer ="your_server_ip";  // Broker ip (raspi) 
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


// SERVO
Servo myservo;
int servo_pin = 2;
int angle = 0;



void setup() {  // START SETUP
  myservo.attach(servo_pin);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
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
    //bool eq = true;
//bool c_eq = true;
    Serial.print("Message arrived at topic: ");
    Serial.println(topic);
    bool eq = true;
    bool c_eq = true;

    // print message
    const char* str = "OPEN";
    const char* c_str = "CLOSE";
    
    Serial.print("Message:");
    // OPEN MSG COMPARISON
    for (int i=0; i<length; i++) { // fucking c shit comparison
      Serial.print((char)payload[i]);
      if ( (char)payload[i] != str[i]) { // checking for OPEN command
        // Serial.print("Equals");
        eq = false;
      }
      // strcat(str*, (char)payload[i]);
    }
    if (eq) {
      open_the_lock = true;
    }
    // CLOSE MSG COMPARISON
    for (int i=0; i<length; i++) { // fucking c shit comparison
      Serial.print((char)payload[i]);
      if ( (char)payload[i] != c_str[i]) { // checking for OPEN command
        // Serial.print("Equals");
        c_eq = false;
      }
      // strcat(str*, (char)payload[i]);
    }
    if (c_eq) {
      close_the_lock = true;
      //c_eq = false;
    }
    Serial.print("In one conversion => ");
    // String str = (char*) payload;
    // char* str  = (char*)payload;
    Serial.println(str);
    Serial.println();
    Serial.print("----------");
  }


void Blink() {
         // wait for a 0.5 second
           //digitalWrite(LED_BUILTIN, LOW);
  //delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
}

void closeLock(){
  Blink();
   //move from 180 to 0 degrees with a negative angle of 5
  for(angle = 180; angle>=1; angle-=5)
  {                                
    myservo.write(angle);
    delay(5);                       
  } 
      delay(1000);
}

// --- OPEN LOCK LOGIC HERE ---
void openLock(){
  
  Serial.print("ITS ON");       
  Serial.print("=>  LOCK OPENED  <=");
  Blink();
   //move from 0 to 180 degrees with a positive angle of 1
  for(angle = 0; angle < 180; angle += 5)
  {                          
    myservo.write(angle);
    delay(15);                       
  } 

  delay(1000);
}

const int PUBLISH_INTERVAL = 2000;
void loop() { // keep publishing state at regular intervals
  if(open_the_lock) {
    openLock();
    open_the_lock = false;
  }

  if(close_the_lock) {
    closeLock();
    close_the_lock = false;
  }
 
  client.loop();
  client.publish(ADV_CHANNEL, ID); // for now keep sending your ID
  // Serial.println("Published message TO ADV--");
  client.publish(STATE_CHANNEL, STATE); // keep sending state 
  delay(PUBLISH_INTERVAL);
}
