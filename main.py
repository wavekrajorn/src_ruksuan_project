import serial
import time
import requests

# Configure the serial connection (replace with your serial port and baud rate)
ser = serial.Serial('COM7', 9600)  # For Windows, use 'COM3' or other port; for Linux, use '/dev/ttyUSB0' or similar

last_message = None
last_time = 0
delay = 60  # Delay in seconds before allowing the same message to be processed again

def send_Notify_Fire():
    url = "http://localhost:3000/notifyFire"
    try:
        response = requests.post(url)
        print(f"Request sent. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def send_Notify_Gas():
    url = "http://localhost:3000/notifyGas"
    try:
        response = requests.post(url)
        print(f"Request sent. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def send_Notify_Quake():
    url = "http://localhost:3000/notifyQuake"
    try:
        response = requests.post(url)
        print(f"Request sent. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def send_Notify_WaterMid():
    url = "http://localhost:3000/notifyWaterMid"
    try:
        response = requests.post(url)
        print(f"Request sent. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def send_Notify_WaterHigh():
    url = "http://localhost:3000/notifyWaterHigh"
    try:
        response = requests.post(url)
        print(f"Request sent. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")


def handle_message(message):
    if message == "Water level mid!":
        send_Notify_WaterMid()
    elif message == "Water level high!":
        send_Notify_WaterHigh()
    elif message == "Gas detected!":
        send_Notify_Gas()
    elif message == "Fire detected!":
        send_Notify_Fire()
    elif message == "Vibration detected!":
        send_Notify_Quake()
    else:
        print("Unhandled message: ", message)

while True:
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').strip()  # Read the message and decode it

        current_time = time.time()
        
        if message != last_message or (current_time - last_time) > delay:
            handle_message(message)
            last_message = message
            last_time = current_time
        else:
            print(f"Ignored duplicate message: {message}")
