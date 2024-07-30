# // Craft By : Vish Siriwatana

import face_recognition
import cv2
import os
import pickle
import time
import json

# Load configuration
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

config = load_config()

# Directory to save detected faces and history
output_dir = "detected_faces"
os.makedirs(output_dir, exist_ok=True)

# File path to load the trained model
model_path = "trained_model.pkl"

# Load face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load the trained model
def load_model():
    global known_face_encodings, known_face_names
    if os.path.exists(model_path):
        with open(model_path, 'rb') as model_file:
            known_face_encodings, known_face_names = pickle.load(model_file)
        print(f"Model loaded from {model_path}")
    else:
        print("No model found. Exiting.")
        exit()

load_model()

# Initialize video capture
video_capture = cv2.VideoCapture(0)

process_every_n_frames = 2
frame_count = 0

if config.get("enable_history_logging", False):
    history_log_path = os.path.join(output_dir, "history.log")
    history_log = open(history_log_path, "a")
else:
    history_log = None

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if frame_count % process_every_n_frames == 0:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            top, right, bottom, left = face_location
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            if config.get("enable_auto_photo", False):
                face_image = frame[top:bottom, left:right]
                face_image_resized = cv2.resize(face_image, (200, 200))

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                face_image_path = os.path.join(output_dir, f"{name}_{timestamp}.jpg")
                cv2.imwrite(face_image_path, face_image_resized)

                if history_log:
                    history_log.write(f"{timestamp}: {name} detected and saved as {face_image_path}\n")
                    history_log.flush()

            face_names.append(name)

    frame_count += 1

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

if history_log:
    history_log.close()