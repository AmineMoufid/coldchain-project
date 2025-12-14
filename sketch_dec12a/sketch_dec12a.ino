#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Wifi_Perso_2.4G";
const char* pass = "FC73FBCB235E";
const char* url  = "http://192.168.1.14:8000/api/post_data/"; // Change IP

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if(isnan(t) || isnan(h)) { 
    Serial.println("Failed to read DHT"); 
    return; 
  }

  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, url);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"sensor_id\":1,\"temperature\":" + String(t,1) +
                  ",\"humidity\":" + String(h,1) + "}";
    int code = http.POST(json);
    Serial.println("POST HTTP code: " + String(code));
    http.end();
  }

delay(1200000); // 20 minutes
}
