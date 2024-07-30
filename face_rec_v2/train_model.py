# // Craft By : Vish Siriwatana

import face_recognition
import cv2
import os
import pickle

# Directory containing member images
member_dir = "members"
# File path to save the trained model
model_path = "trained_model.pkl"

# Load face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize lists for face encodings and names
known_face_encodings = []
known_face_names = []

# Train the model
for member in os.listdir(member_dir):
    member_path = os.path.join(member_dir, member)
    for image_file in os.listdir(member_path):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            image_path = os.path.join(member_path, image_file)
            print(f"Processing {image_path}")
            
            member_image = cv2.imread(image_path)
            if member_image is None:
                print(f"Failed to read {image_path}")
                continue

            rgb_image = cv2.cvtColor(member_image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            for face_location in face_locations:
                try:
                    face_encoding = face_recognition.face_encodings(rgb_image, [face_location])[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(member)
                except IndexError:
                    print(f"Failed to encode face at {image_path}")
                    continue

# Save the trained model
with open(model_path, 'wb') as model_file:
    pickle.dump((known_face_encodings, known_face_names), model_file)

print(f"Model saved to {model_path}")
