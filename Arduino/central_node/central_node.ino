
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <Firebase_ESP_Client.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include "PubSubClient.h"
#include <IRremoteESP8266.h>
#include <IRsend.h>
// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

const uint16_t kIrLed = 0; 
IRsend emissorIR(kIrLed);
#define tempoTecla 350

#define WIFI_SSID "DORETOALENCAR"
#define WIFI_PASSWORD "123MDAfamilia"

const char* mqtt_server = "192.168.0.173";  // IP of the MQTT broker
int mqtt_port = 1883;  // PORTA of the MQTT broker
const char* clientID = "nodemcu"; // MQTT client ID
const char* command_topic = "NodeMcu";
WiFiClient espClient;                                                   
PubSubClient client_mqtt(espClient);

// Insert Firebase project API Key
#define API_KEY "AIzaSyBvy9KIICtW5qR374kCZ8d9TK4Twa8fq-o"

// Insert Authorized Email and Corresponding Password
#define USER_EMAIL "matheusdoreto.md@gmail.com"
#define USER_PASSWORD "24861793"

// Insert RTDB URLefine the RTDB URL
#define DATABASE_URL "https://jarvis-sqri-default-rtdb.firebaseio.com/"

#define SEALEVELPRESSURE_HPA (1013.25)
// Define Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Variable to save USER UID
String uid;
String databasePath;
// Variables to save database paths

// BME280 sensor
Adafruit_BME280 bme; // I2C
float temperature;
float humidity;
float pressure;
float altitude;
int ldrValue;
signed long rssi;

// Timer variables (send new readings every three minutes)
unsigned long sendDataPrevMillis = 0;
unsigned long timerDelay = 60000;

// Initialize BME280
void initBME(){
  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}



void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    String message;
    char command = (char) payload[0];
    for (int i = 0; i < length; i++) {
        message = message + (char) payload[i];  // convert *byte to string
    }
    Serial.print(command);
    sendSignal(command);
    
    Serial.println();
    Serial.println("-----------------------");
}
void initMQTT(){  
  client_mqtt.setServer(mqtt_server, mqtt_port);                                  
  client_mqtt.setCallback(callback);
   while (!client_mqtt.connected()) {
        String client_id = "esp8266-client-";
        client_id += String(WiFi.macAddress());
        Serial.println("Connecting to public emqx mqtt broker.....");
        if (client_mqtt.connect(clientID)) {
            Serial.println("Public emqx mqtt broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.print(client_mqtt.state());
            delay(2000);
        }      }
  client_mqtt.subscribe(command_topic); 
  client_mqtt.publish(command_topic, "hello emqx");
  
}
// Initialize WiFi
void initWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
  Serial.println();
}
void initOTA(){
  ArduinoOTA.onStart([]() {
    Serial.println("Inicio...");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("nFim!");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progresso: %u%%r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Erro [%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Autenticacao Falhou");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Falha no Inicio");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Falha na Conexao");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Falha na Recepcao");
    else if (error == OTA_END_ERROR) Serial.println("Falha no Fim");
  });
  ArduinoOTA.begin();
  Serial.println("Pronto");
  Serial.print("Endereco IP: ");
  Serial.println(WiFi.localIP());
}

// Write float values to the database
void sendFloat(){

FirebaseJson json;
json.set("temperature", temperature);
json.set("humidity", humidity);
json.set("pressure", pressure);
json.set("timestamp/.sv", "timestamp");
 if (Firebase.RTDB.push(&fbdo, "/NodeMcu/bme280/", &json)){
    Serial.print("Writing value: ");
    Serial.print(" on the following path: ");

    Serial.println("PASSED");

    Serial.println("TYPE: " + fbdo.dataType());
  }
  else {
    Serial.println("FAILED");
    Serial.println("REASON: " + fbdo.errorReason());
  }
  
}
void sendStaticFloat(String path, float value){
  if (Firebase.RTDB.setFloat(&fbdo, "/NodeMcu/" +path, value)){
    Serial.print("Writing value: ");
    Serial.print (value);
    Serial.print(" on the following path: ");

    Serial.println("PASSED");

    Serial.println("TYPE: " + fbdo.dataType());
  }
  else {
    Serial.println("FAILED");
    Serial.println("REASON: " + fbdo.errorReason());
  }
}

void setup(){
  Serial.begin(115200);

  // Initialize BME280 sensor
  initBME();
  initWiFi();
  initOTA();
  initMQTT();

  // Assign the api key (required)
  config.api_key = API_KEY;

  // Assign the user sign in credentials
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  // Assign the RTDB URL (required)
  config.database_url = DATABASE_URL;

  Firebase.reconnectWiFi(true);
  fbdo.setResponseSize(4096);

  // Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  // Assign the maximum retry of token generation
  config.max_token_generation_retry = 5;

  // Initialize the library with the Firebase authen and config
  Firebase.begin(&config, &auth);

  // Getting the user UID might take a few seconds
  Serial.println("Getting User UID");
  while ((auth.token.uid) == "") {
    Serial.print('.');
    delay(1000);
  }
  // Print user UID
  uid = auth.token.uid.c_str();
  Serial.print("User UID: ");
  Serial.println(uid);
  emissorIR.begin();
  // Update database path
  databasePath = "/NodeMcu";

  // Update database path for sensor readings
}

void loop(){
  // Send new readings to database
  if (Firebase.ready() && (millis() - sendDataPrevMillis > timerDelay || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();

    // Get latest sensor readings
    temperature = bme.readTemperature();
    humidity = bme.readHumidity();
    pressure = bme.readPressure()/100.0F;
    altitude = bme.readAltitude(SEALEVELPRESSURE_HPA);
    // Send readings to database:
    sendFloat();
    sendStaticFloat("altitude/",altitude);
    ldrValue = analogRead(A0); 
    sendStaticFloat("light/",ldrValue);
    rssi = WiFi.RSSI();
    sendStaticFloat("rssi/",rssi);
  }
  client_mqtt.loop();
  ArduinoOTA.handle();
}
void switchLight() { 
  int ldrValue = analogRead(A0);
  emissorIR.sendNEC(0xFF02FD, 32);
  delay(200);
  if (abs(ldrValue - analogRead(A0)) <10)
  {
    emissorIR.sendNEC(0xFF9867, 32);
    }
}
void sendSignal(char s)
{
  digitalWrite(LED_BUILTIN, LOW);

  switch (s) {
    case 'c':
      emissorIR.sendNEC(0x8E7807F, 32);
      Serial.println("Power Caixa de Som");
      delay(tempoTecla);
      break;

    case 'b':
      emissorIR.sendNEC(0x8E750AF, 32);
      Serial.println("bluetooth caixa de som");
      delay(tempoTecla);
      break;
    case 'l':
      emissorIR.sendNEC(0x8E7A857, 32);
      Serial.println("linha caixa de som");
      delay(tempoTecla);
      break;
    case '+':
      emissorIR.sendNEC(0x8E7906F, 32);
      Serial.println("volume + caixa de som");
      delay(tempoTecla);
      break;

    case '-':
      emissorIR.sendNEC(0x8E730CF, 32);
      Serial.println("volume- caixa de som");
      delay(tempoTecla);
      break;

    case 't':
      emissorIR.sendNEC(0x20DF10EF, 32);
      Serial.println("Power TV");
      delay(tempoTecla);
      break;

    case 'n':
      emissorIR.sendNEC(0xE17A48B7, 32);
      Serial.println("power net");
      delay(tempoTecla);
      break;

    case '1':
      emissorIR.sendNEC(0xE17A807F, 32);
      Serial.println("1");
      delay(tempoTecla);
      break;
    case '2':
      emissorIR.sendNEC(0xE17A40BF, 32);
      Serial.println("2");
      delay(tempoTecla);
      break;

    case '3':
      emissorIR.sendNEC(0xE17AC03F, 32);
      Serial.println("3");
      delay(tempoTecla);
      break;

    case '4':
      emissorIR.sendNEC(0xE17A20DF, 32);
      Serial.println("4");
      delay(tempoTecla);
      break;
    case '5':
      emissorIR.sendNEC(0xE17AA05F, 32);
      Serial.println("5");
      delay(tempoTecla);
      break;
    case '6':
      emissorIR.sendNEC(0xE17A609F, 32);
      Serial.println("6");
      delay(tempoTecla);
      break;
    case '7':
      emissorIR.sendNEC(0xE17AE01F, 32);
      Serial.println("7");
      delay(tempoTecla);
      break;
    case '8':
      emissorIR.sendNEC(0xE17A10EF, 32);
      Serial.println("8");
      delay(tempoTecla);
      break;
    case '9':
      emissorIR.sendNEC(0xE17A906F, 32);
      Serial.println("9");
      delay(tempoTecla);
      break;
    case '0':
      emissorIR.sendNEC(0xE17A00FF, 32);
      Serial.println("0");
      delay(tempoTecla);
      break;
    case '>':
      emissorIR.sendNEC(0xE17AB04F, 32);
      Serial.println("+ volume net");
      delay(tempoTecla);
      break;
    case '<':
      emissorIR.sendNEC(0xE17A708F, 32);
      Serial.println("- volume net");
      delay(tempoTecla);
      break;
    case 's':
      emissorIR.sendNEC(0x20DF1EE1, 32);
      Serial.println("SearchTv");
      delay(tempoTecla);
      break;
    case 'a':
      switchLight();
      Serial.println("switch luz");
      delay(tempoTecla);
      break;
    case 'p':
      emissorIR.sendNEC(0xE17A7887, 32);
      Serial.println("Programação NET");
      delay(tempoTecla);
      break;
    case 'v':
      emissorIR.sendNEC(0xE17A8877, 32);
      Serial.println("Voltar NET");
      delay(tempoTecla);
      break;
  }
  digitalWrite(LED_BUILTIN, HIGH);
}
