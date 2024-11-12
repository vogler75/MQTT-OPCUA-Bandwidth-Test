import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import time
import os

# Define the MQTT broker and topic
broker = 'linux0'
port = 1883
topic = "Enterprise/#"

# Global variable to keep track of the number of messages received
message_counter = 0


# Define the callback function for when a message is received
def on_message(client, userdata, message):
    global message_counter
    message_counter += 1
    #print(f"Received message: {len(message.payload)} on topic {message.topic}")


# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")


if __name__ == "__main__":
    print(f"My PID is: {os.getpid()}")

    # Create an MQTT client instance
    client = mqtt.Client(protocol=mqtt.MQTTv5)

    connect_properties = Properties(PacketTypes.CONNECT)
    connect_properties.TopicAliasMaximum = 10000

    # Assign the on_message and on_connect callback functions
    client.on_message = on_message
    client.on_connect = on_connect

    # Connect to the MQTT broker
    client.connect(broker, port, 60, properties=connect_properties)
    client.loop_start()

    while True:
        time.sleep(1)
        print(f"Messages received: {message_counter}")
