#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>


const char * ssid = "";
const char * password = "";

// MQTT Broker
IPAddress mqtt_broker(192, 168, 0, 55);
const char * topic = "esp8266/tomato";
const char * topic_sensor = "esp8266/tomato_sensor";

// MQTT Broker username and password incase your broker need them
const char * mqtt_username = "";
const char * mqtt_password = "";
const int mqtt_port = 1883;
char msg[30];

const int pump_pin = 16;
bool pump_running = false;
int moisture_level = 0;
unsigned long last_sensor_reading_time = 0;
unsigned long pump_start_time = 0;


WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {

  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    client_id += String(millis());
    Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Public emqx mqtt broker connected");
      break;
    } else {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe(topic_sensor);
}

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  pinMode(pump_pin, OUTPUT);

  delay(10);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WIFI...");
  }
  Serial.println("WiFi connected");
  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
}

void turn_on_pump() {
  Serial.println("Turning on pump");
  pump_running = true;
  pump_start_time = millis();
  client.publish(topic, "PUMP_START");
  digitalWrite(pump_pin, HIGH);
}

void turn_off_pump() {
  Serial.println("Turning off pump");
  pump_running = false;
  client.publish(topic, "PUMP_STOP");
  digitalWrite(pump_pin, LOW);
}

void callback(char * t, byte * payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(t);
  Serial.println("Message:");
  String message;
  for (int i = 0; i < length; i++) {
    Serial.print((char) payload[i]);
    message += (char) payload[i];
  }
  Serial.println();

  if (message == "PUMP_START") {
    turn_on_pump();
  } else if (message == "PUMP_STOP") {
    turn_off_pump();
  }

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  //when pump is not running take moisture level every 2 minutes
  if (!pump_running) {

    if (last_sensor_reading_time == 0 || millis() > last_sensor_reading_time + (2 * 60 * 1000)) {
      int sensor_reading = analogRead(A0);
      last_sensor_reading_time = millis();

      Serial.print("Moisture Sensor Value: ");
      Serial.println(sensor_reading);
      moisture_level = map(sensor_reading, 900, 300, 0, 100);
      if (moisture_level < 30) {
        turn_on_pump();
      }
      sprintf(msg, "%d", sensor_reading);
      client.publish(topic, msg);
    }

  } else {
    //when pump is  running take moisture level every 45 seconds
    if (last_sensor_reading_time == 0 || millis() > last_sensor_reading_time + (45 * 1000)) {
      int sensor_reading = analogRead(A0);
      moisture_level = map(sensor_reading, 900, 300, 0, 100);
      //run the pump atleast 1 min before turning it off.
      if (moisture_level >= 75 && millis() >= pump_start_time + (60*1000)) {
        turn_off_pump();
      }
    }
  }

  client.publish(topic, "NOOP");
  client.loop();
}
