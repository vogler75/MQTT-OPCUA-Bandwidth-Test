import csv
import json
import time
import random
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

# MQTT broker details
broker = 'linux0'
port = 1883

# Topics file
topic_file = 'topics.csv'

# Sleep times
sleep_time = 0  # seconds to sleep between publishing to topics
sleep_time_loop = 1  # seconds to sleep between a full loop of all topics


# Read topics from CSV file
def read_topics(file_path):
    topics = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            topics.append(row[0])
    return topics


# Publish to MQTT topics
def publish_to_topics(client, topics):
    for topic in topics:
        value = random.randint(1, 1000)
        payload = {"TimeMS": int(time.time() * 1000), "Value": value}
        client.publish(topic, json.dumps(payload), retain=False, qos=0)
        client.publish("Binary/"+topic, value.to_bytes(4, byteorder='big'), retain=False)
        #print(f'Published to {topic}: {payload}')
        time.sleep(sleep_time)


# MQTT on_connect callback
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print('Connected to MQTT broker')
        client.subscribe('Enterprise/SimDelay', 0)
    else:
        print(f'Failed to connect, return code {rc}')


def on_message(client, userdata, msg):
    global sleep_time_loop
    try:
        sleep_time_loop = float(msg.payload.decode())
        print(f'Received SimDelay: {sleep_time_loop}')
    except ValueError:
        print('Failed to convert message payload to float')


# Main function
def main():
    global publish_value
    topics = read_topics(topic_file)

    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message

    connect_properties = Properties(PacketTypes.CONNECT)
    connect_properties.TopicAliasMaximum = 10000

    client.connect(broker, port, 60, properties=connect_properties)
    client.loop_start()

    while not client.is_connected():
        time.sleep(1)

    while True:
        publish_to_topics(client, topics)
        time.sleep(sleep_time_loop)

    client.loop_stop()
    client.disconnect()


if __name__ == '__main__':
    main()
