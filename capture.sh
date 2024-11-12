#!/bin/bash

server_ip=192.168.1.3

# Get the process ID of mqttsubscribe
mqtt_pid=$(ps -ef | grep -i mqttsubscribe | grep -v grep | awk '{print $2}')

# Get the process ID of opcsubscribe
opc_pid=$(ps -ef | grep -i opcsubscribe | grep -v grep | awk '{print $2}')

echo MQTT: $mqtt_pid
echo OPC: $opc_pid

# Check if PIDs were found
if [ -z "$mqtt_pid" ] || [ -z "$opc_pid" ]; then
  echo "Could not find mqttsubscribe or opcsubscribe process."
  exit 1
fi

# Get the port numbers for each process using netstat
mqtt_port=$(netstat -ap 2>/dev/null | grep "$mqtt_pid" | grep $server_ip:1883 | awk '{print $4}' | sed 's/.*://')
opc_port=$(netstat -ap 2>/dev/null | grep "$opc_pid" | grep $server_ip:4840 | awk '{print $4}' | sed 's/.*://')

# Output the port numbers
echo "MQTT Port: $mqtt_port"
echo "OPC UA Port: $opc_port"

rm -f capture-*.pcap
sudo tcpdump -i eth0 port $mqtt_port -w capture-mqtt.pcap &
sudo tcpdump -i eth0 port $opc_port -w capture-opc.pcap &
