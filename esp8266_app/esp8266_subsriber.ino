# include <ESP8266WiFi.h>
# include <PubSubClient.h>

const char* ssid = "PLANET_007";
const char* password = "hamatari";
const char* mqttServer ="192.168.1.7";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

// client
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
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
  while(!client.connected()) {
    Serial.println("Connecting to MQTT ...");
    if (client.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed to connect with state");
      Serial.print(client.state());
      delay(2000);
    }
  }
  
  client.publish("test_channel", "hello raspi channel");
  client.subscribe("esp/data");

}

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

void loop() {
  client.loop();
  client.publish("test_channel", "hello raspi channel");
  delay(1000);
}
