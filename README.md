# MQTT and OPC UA Bandwidth Test Tool

This project provides a set of tools to test the bandwidth usage of MQTT and OPC UA protocols by simulating a full topic tree and monitoring network traffic. It includes a Docker Compose environment for easy deployment, a simulation tool for generating data, and subscribers to measure the bandwidth consumed by both protocols.

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Components](#components)
  - [Docker Compose Services](#docker-compose-services)
  - [Simulator](#simulator)
  - [Subscribers](#subscribers)
- [How to Use](#how-to-use)
- [Monitoring Network Traffic](#monitoring-network-traffic)

## Overview
The MQTT and OPC UA Bandwidth Test Tool helps assess the network traffic generated when transforming an MQTT topic tree into an OPC UA server using the Frankenstein automation gateway. The Python client programs allow for testing and comparing the bandwidth requirements of both protocols.

The data format used for MQTT is JSON, containing a timestamp and a value. This format is required for the Frankenstein gateway to transform the MQTT topic tree into the OPC UA server correctly.

## Setup

Note: Network traffic is easier to track if you run the servers and the clients (opcsubscriber/mqttsubscriber) on different machines! And run nethogs at the client machine.

### Prerequisites
- Docker and Docker Compose installed.
- Python 3 installed.
- A Linux environment to use network monitoring tools like NetHogs (optional, but recommended).

### Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Start the Docker environment with MQTT broker and Frankenstein automation gateway:
   ```sh
   docker-compose up -d
   ```
3. Install Python dependencies (e.g., paho-mqtt, opcua, etc.) if required:
   ```sh
   pip install -r requirements.txt
   ```

## Components

### Docker Compose Services
The project includes a `docker-compose.yaml` file that sets up the following services:

1. **MQTT Broker**: A lightweight broker to publish data from the simulator.
2. **Frankenstein Automation Gateway**: A gateway that converts the MQTT topic tree into an OPC UA server, making the data available via OPC UA for the subscribers.

The gateway requires data in JSON format containing a `timestamp` and `value` fields to successfully transform the MQTT data to OPC UA nodes.

### Simulator
- **simulator.py**: Simulates the entire topic tree and generates data for testing. The generated data is published to the MQTT broker in JSON format with a `timestamp` and `value`.

### Subscribers
- **mqttsubscriber.py**: Connects to the MQTT broker and subscribes to the entire topic tree. The program can be used to measure the bandwidth used by MQTT subscriptions.
- **opcsubscriber.py**: Connects to the OPC UA server and browses the entire topic tree, then creates subscriptions for all available nodes. This subscriber allows for measuring the bandwidth used by OPC UA subscriptions.

## How to Use

1. **Start the Docker Environment**
   Run the Docker Compose setup to start the MQTT broker and Frankenstein automation gateway:
   ```sh
   docker-compose up -d
   ```
   Before you run it, adapt the config-frankenstein.yml and set your IP-Address:
   ```yaml
   Servers:
     OpcUa:
       - Port: 4840
         Enabled: true
         LogLevel: INFO
         EndpointAddresses:
           - "linux0" # CHANGE THIS TO YOUR HOST IP
         Topics:
           - Topic: mqtt/test/path/Enterprise/#         
   ```

2. **Run the Simulator**
   Start the simulator to generate the topic tree with simulated data:
   ```sh
   python simulator.py
   ```

3. **Run Subscribers**
   - Run the MQTT subscriber:
     ```sh
     python mqttsubscriber.py
     ```
   - Run the OPC UA subscriber:
     ```sh
     python opcsubscriber.py
     ```

4. **Monitor Network Traffic**
   Use a tool like NetHogs on Linux to monitor the network usage of each program:
   ```sh
   sudo nethogs
   ```
   You can use NetHogs to observe the bandwidth consumption of `mqttsubscriber.py`, `opcsubscriber.py`, and the simulator to determine the impact of each communication protocol.

## Monitoring Network Traffic
To effectively analyze the network bandwidth used by MQTT and OPC UA protocols, you can use the following steps:

- **NetHogs**: NetHogs provides an easy way to visualize bandwidth usage by each program.
- Install NetHogs:
  ```sh
  sudo apt-get install nethogs
  ```
- Run NetHogs while the simulation and subscribers are active:
  ```sh
  sudo nethogs
  ```
  This will show real-time network usage for `simulator.py`, `mqttsubscriber.py`, and `opcsubscriber.py`. Compare the network usage for MQTT and OPC UA to understand their respective bandwidth demands.

## Notes
- The JSON format for MQTT messages is mandatory for the correct operation of the Frankenstein gateway.
- Ensure Docker and Python dependencies are correctly installed before running the tool.

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.

## Contact
For any questions or issues, please open an issue in the repository.

