from opcua import Client, ua
import time
import os

# Define the OPC UA server URL and the root node to subscribe to
server_url = "opc.tcp://linux0:4840/server"
root_node_id = "ns=2;s=85/Mqtt/test/Enterprise"  # Replace with the actual node ID you want to subscribe to

# Global variable to keep track of the number of messages received
message_counter = 0


def browse_and_subscribe(client, node):
    global handler, subscripiton
    if node.get_node_class() == ua.NodeClass.Variable:
        # Subscribe to the node
        handle = subscription.subscribe_data_change(node)
        #print(f"Subscribed to node: {node}")

    # Browse the node to get all its children
    children = node.get_children()
    for child in children:
        browse_and_subscribe(client, child)


class SubHandler(object):
    def datachange_notification(self, node, val, data):
        global message_counter
        #print(f"Data change on node {node}: {val}")
        message_counter += 1

    def event_notification(self, event):
        print(f"Event: {event}")


if __name__ == "__main__":
    print(f"My PID is: {os.getpid()}")
    client = Client(server_url)
    try:
        client.connect()
        print("Connected to OPC UA server")
        handler = SubHandler()
        subscription = client.create_subscription(500, handler)
        root_node = client.get_node(root_node_id)
        browse_and_subscribe(client, root_node)

        print("Subscribe done.")

        while True:
            time.sleep(1)
            print(f"Messages received: {message_counter}")
    finally:
        client.disconnect()
        print("Disconnected from OPC UA server")