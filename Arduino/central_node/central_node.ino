
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

#define WIFI_SSID "DORETOALENCAR"
#define WIFI_PASSWORD "123MDAfamilia"

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
}
