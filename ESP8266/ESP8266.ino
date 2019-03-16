#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "Red Prueba"
#define STAPSK  "prueba1234"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

const int led = 13;
String state_led;

void prender() {
  analogWrite(led, 255);
  state_led = "On";
  server.send(200, "text/plain", "Prendio");
}

void apagar() {
  analogWrite(led, 0);
  state_led =  "Off";
  server.send(200, "text/plain", "Apago");
}

void state() {
  server.send(200, "text/plain", state_led);
}
void handleNotFound() {
  String message = "File Not Found";
  server.send(404, "text/plain", message);
}

void setup(void) {
  pinMode(led, OUTPUT);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/on", prender);
  server.on("/off", apagar);
  server.on("/state", state);

  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}
