# // Craft By : Vish Siriwatana

import face_recognition
import cv2
import os
import pickle
import time
import json
import numpy as np  # Import NumPy
import requests  # Import requests for HTTP requests
import base64

# Load configuration
def load_config():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found. Please create 'config.json' with necessary configurations.")
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

try:
    config = load_config()
except Exception as e:
    print(f"Error loading configuration: {e}")
    exit(1)

# Directory to save detected faces and history
output_dir = "detected_faces"
os.makedirs(output_dir, exist_ok=True)

# File path to load the trained model
model_path = "trained_model.pkl"

# Load the trained model
def load_model():
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found. Please ensure 'trained_model.pkl' exists and is accessible.")
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)

try:
    known_face_encodings, known_face_names = load_model()
    print(f"Model loaded from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Function to send base64 image to the API
def send_to_api(base64_image):
    url = "http://localhost:3000/notifyPeople"

    payload = { "image64": base64_image }
    headers = {"content-type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())

# Initialize video capture
video_capture = cv2.VideoCapture(0)

process_every_n_frames = 2
frame_count = 0

history_log_path = os.path.join(output_dir, "history.log")
history_log = None
if config.get("enable_history_logging", False):
    history_log = open(history_log_path, "a")

# Variable to track last notification time
last_notification_time = 0
notification_delay = 180  # Delay in seconds (3 minutes)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture video frame.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if frame_count % process_every_n_frames == 0:
        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compute the distance between the current face and known faces
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            name = "Unknown"
            if face_distances[best_match_index] < 0.45:  # You can adjust this threshold
                name = known_face_names[best_match_index]

            top, right, bottom, left = face_location
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Automatically save detected face image if enabled
            face_image_path = None
            if config.get("enable_auto_photo", False) or name == "Unknown":
                face_image = frame[top:bottom, left:right]
                face_image_resized = cv2.resize(face_image, (200, 200))

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                face_image_path = os.path.join(output_dir, f"{name}_{timestamp}.jpg")
                cv2.imwrite(face_image_path, face_image_resized)

                if history_log:
                    history_log.write(f"{timestamp}: {name} detected and saved as {face_image_path}\n")
                    history_log.flush()

            face_names.append(name)

            # Send notification if the face is unknown and delay has passed
            current_time = time.time()
            if name == "Unknown" and (current_time - last_notification_time) > notification_delay:
                message = "Unknown person detected!"
                _, buffer = cv2.imencode('.jpg', face_image)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                send_to_api(base64_image)
                last_notification_time = current_time

    frame_count += 1

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

if history_log:
    history_log.close()
