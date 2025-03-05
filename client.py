import cv2
import socket
import pickle
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Send video frames to a server.")
parser.add_argument('serverip', nargs='?', default='10.42.0.1', help="IP address of the server (default: 10.42.0.1)")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000) 
args = parser.parse_args()

serverip = args.serverip  # Use the provided server IP or default
serverport = 5000       # Port number should be same for client and server

# OpenCV camera capture
cap = cv2.VideoCapture(0)  # 0 for the default webcam, change if you have multiple cameras

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set the camera format to MJPEG
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Set a standard resolution (640x480 or any suitable lower resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # Set height

# Check the actual resolution set
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution set to: {width}x{height}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Ensure the frame size is reasonable
    if frame is None or frame.size == 0:
        print("Empty or corrupted frame!")
        continue

    # Debugging: Print the resolution of each frame
    print(f"Captured frame resolution: {frame.shape[1]}x{frame.shape[0]}")

    if frame.shape[0] > 65500 or frame.shape[1] > 65500:
        print("Invalid frame size, skipping...")
        continue

    # Encode the image as JPEG with quality optimization
    ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    if ret:
        x_as_bytes = pickle.dumps(buffer)  # Convert buffer to bytes
        s.sendto(x_as_bytes, (serverip, serverport))  # Send the byte stream to the server
    else:
        print("Error encoding frame.")

cap.release()  # Release the camera when done
