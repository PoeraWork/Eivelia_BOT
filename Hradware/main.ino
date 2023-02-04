#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char *ssid = "Eivelia's";
const char *password = "99990000";
const char *mqtt_server = "broker.mqtt-dashboard.com";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int ii = 0;

void wifi_conn();
void reconnect();

void setup()
{
    //pinMode(BUILTIN_LED, OUTPUT);
    Serial.begin(115200);
    wifi_conn();
    client.setServer(mqtt_server, 1883);
    pinMode(D8, OUTPUT);
    pinMode(D5, INPUT_PULLUP);
    pinMode(D2, INPUT_PULLUP);
}

void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();

    unsigned long now = millis();
    if (now - lastMsg > 2000)
    {
        lastMsg = now;

        if (digitalRead(D5) == HIGH)
        {
            
            ++ii;
            Serial.print("Publish message: ");
            Serial.println(msg);
            client.publish("baojing", msg);
            
            digitalWrite(D8, HIGH);
            snprintf(msg, MSG_BUFFER_SIZE, "ON FIRE! #%ld", ii);
        }
        if (digitalRead(D5) == LOW)
        {
            digitalWrite(D8, LOW);
            // snprintf(msg, MSG_BUFFER_SIZE, "SECURE #%ld", ii);
            Serial.print("SECURE\n");
        }
        if (digitalRead(D2) == LOW)
        {
            ++ii;
            Serial.print("Publish message: ");
            Serial.println(msg);
            client.publish("baojing", msg);

            digitalWrite(D8, HIGH);
            snprintf(msg, MSG_BUFFER_SIZE, "GAS LEAK! #%ld", ii);
        }
    }
}

void wifi_conn()
{
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str()))
        {
            Serial.println("connected");
            client.publish("outTopic", "hello world");
            client.subscribe("inTopic");
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
