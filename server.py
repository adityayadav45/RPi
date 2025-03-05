#!/usr/bin/python3

import cv2
import socket
import numpy as np
import pickle
import argparse

# Set up argument parser to accept IP as an argument
parser = argparse.ArgumentParser(description="UDP Video Stream Server")
parser.add_argument("ip", nargs="?", default="10.42.0.1", help="IP address of the server to bind")
args = parser.parse_args()

# Assign the provided IP address to the variable 'ip'
ip = args.ip  # Server IP (the one you're receiving the stream on)
port = 5000  # Same port number as client

# Set up the UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Using UDP protocol

# Bind the server to the specified IP and port
s.bind((ip, port))

# Start an infinite loop to receive and display frames
while True:
    # Receive data sent by the client
    x = s.recvfrom(100000000)  # The buffer size can be adjusted as needed
    client_ip = x[1][0]  # Get client IP from the received message
    data = x[0]  # The byte data sent by the client
    
    # Deserialize the received byte data into a Numpy array
    data = pickle.loads(data)  # Convert byte data to Numpy array
    
    # Decode the Numpy array to an image
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)  # Decode the image from Numpy array
    
    # Convert BGR to RGB if needed (OpenCV default is BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Display the decoded frame
    cv2.imshow('Received Video Stream', frame)
    
    # Check if the user pressed Enter (key code 13) to close the window
    if cv2.waitKey(10) == 13:  # 10ms delay for responsiveness
        break

# Clean up and close all OpenCV windows
cv2.destroyAllWindows()

# Close the socket
s.close()


#python3 server.py 10.42.0.154