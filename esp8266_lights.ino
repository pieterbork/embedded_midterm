#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>

Servo Servo1;
Servo Servo2;

const char WiFiSSID[] = "SOC-LAB";
const char WiFiPSK[] = "itpsecurity";

WiFiServer server(80);

void setup() {
  initHardware();
  connectWiFi();
  server.begin();
  setupMDNS();
}
void loop(){
    // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();

  int lightStatus = -1;

  if (req.indexOf("/servo/0") != -1) {
    lightStatus = 0;
    turnOff();
  }
  else if (req.indexOf("/servo/1") != -1) {
    lightStatus = 1;
    turnOn();
  }

  client.flush();

  // Prepare the response. Start with the common header:
  String s = "HTTP/1.1 200 OK\r\n";
  s += "Content-Type: text/html\r\n\r\n";
  s += "<!DOCTYPE HTML>\r\n<html>\r\n";

  // If we're setting the LED, print out a message saying we did
  if (lightStatus >= 0)
  {
    s += "The lights are now ";
    if(lightStatus == 0) {
      s += "off!";
    }
    else if(lightStatus == 1) {
      s += "on!";  
    }
    else {
      s += "idk!";
    }
    s += "<br> <a href=/> home </a>";
  }
  else
  {
    s += "<script src='https://code.jquery.com/jquery-3.3.1.min.js'></script>";
    s += "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>";
    s += "<script>function turnOn() { $.get('/servo/1'); $('.lightStatus').text('Lights are on!') }; function turnOff() { $.get('servo/0'); $('.lightStatus').text('Lights are off!'); };</script>";
    s += "<div class='container'><div class='jumbotron'>";
    s += "<h1>Control the lights in the SOC!</h1><div class='text-right'><i>What a great idea</i></div></div><br><br>";
    s += "Turn lights <button class='btn btn-primary' onclick='turnOn()'> On </button> or <button onclick='turnOff()' class='btn btn-warning'> Off </button> <br><br><br>";
    s += "<div class='lightStatus'></div></div>";
  }
  s += "</html>\n";

  // Send the response to the client
  client.print(s);
  delay(1);
  Serial.println("Client disonnected");
  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

void connectWiFi()
{
  Serial.println();
  Serial.println("Connecting to: " + String(WiFiSSID));
  
  // Set WiFi mode to station (as opposed to AP or AP_STA)
  WiFi.mode(WIFI_STA);

  // WiFI.begin([ssid], [passkey]) initiates a WiFI connection
  // to the stated [ssid], using the [passkey] as a WPA, WPA2,
  // or WEP passphrase.
  WiFi.begin(WiFiSSID, WiFiPSK);

  // Use the WiFi.status() function to check if the ESP8266
  // is connected to a WiFi network.
  while (WiFi.status() != WL_CONNECTED)
  {
    turnOn();
    delay(3000);
    turnOff();

    // Delays allow the ESP8266 to perform critical tasks
    // defined outside of the sketch. These tasks include
    // setting up, and maintaining, a WiFi connection.
    delay(100);
    // Potentially infinite loops are generally dangerous.
    // Add delays -- allowing the processor to perform other
    // tasks -- wherever possible.
  }
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void turnOn() {
  Servo1.write(0);
  Servo2.write(180);  
}

void turnOff() {
  Servo1.write(180);
  Servo2.write(0);  
}

void initHardware()
{
  Serial.begin(9600);
  Servo1.attach(4);
  Servo2.attach(13);
}

void setupMDNS()
{
  if (!MDNS.begin("LIGHT_SWITCH_SERVOS")) 
  {
    Serial.println("Error setting up MDNS responder!");
    while(1) { 
      delay(1000);
    }
  }
  Serial.println("mDNS responder started");

}
