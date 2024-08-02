# // Craft By : Vish Siriwatana

import face_recognition
import cv2
import os
import pickle
import time
from concurrent.futures import ThreadPoolExecutor

# Directory containing member images
member_dir = "members"
# File path to save the trained model
model_path = "trained_model.pkl"

# Load face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize lists for face encodings and names
known_face_encodings = []
known_face_names = []

# Initialize timer
start_time = time.time()

def resize_image(image, width):
    """Resize image to a specific width while maintaining aspect ratio."""
    height = int((width / image.shape[1]) * image.shape[0])
    return cv2.resize(image, (width, height))

def augment_image(image):
    """Apply data augmentation techniques to an image."""
    # Rotate the image slightly to create more variation
    angle = 10  # degrees
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h))
    
    # Flip the image horizontally
    flipped = cv2.flip(image, 1)

    return [image, rotated, flipped]

def process_image(image_path, member, index, total):
    """Process each image to extract face encodings."""
    try:
        print(f"Processing image {index + 1}/{total}: {image_path}")

        member_image = cv2.imread(image_path)
        if member_image is None:
            raise ValueError(f"Failed to read image from {image_path}")

        # Resize image to speed up processing but keep it reasonably large
        rgb_image = cv2.cvtColor(member_image, cv2.COLOR_BGR2RGB)
        rgb_image = resize_image(rgb_image, 800)  # Higher resolution for accuracy

        # Apply data augmentation
        augmented_images = augment_image(rgb_image)

        for augmented_image in augmented_images:
            # Detect faces using CNN model
            face_locations = face_recognition.face_locations(augmented_image, model="cnn")
            if len(face_locations) == 0:
                print(f"No faces found in {image_path}")
                continue

            for face_location in face_locations:
                face_encoding = face_recognition.face_encodings(augmented_image, [face_location])[0]
                return (face_encoding, member)

    except Exception as e:
        print(f"An error occurred processing {image_path}: {e}")
        return None

# Using ThreadPoolExecutor for parallel processing
print("Starting training process...")

image_paths = []
for member in os.listdir(member_dir):
    member_path = os.path.join(member_dir, member)

    if not os.path.isdir(member_path):
        print(f"Skipping non-directory member: {member_path}")
        continue

    for image_file in os.listdir(member_path):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            image_path = os.path.join(member_path, image_file)
            image_paths.append((image_path, member))

total_images = len(image_paths)
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for index, (image_path, member) in enumerate(image_paths):
        futures.append(executor.submit(process_image, image_path, member, index, total_images))

    for future in futures:
        result = future.result()
        if result:
            known_face_encodings.append(result[0])
            known_face_names.append(result[1])

# Save the trained model
with open(model_path, 'wb') as model_file:
    pickle.dump((known_face_encodings, known_face_names), model_file)

# Calculate total time
end_time = time.time()
training_duration = end_time - start_time

print(f"Model saved to {model_path}")
print(f"Training completed in {training_duration:.2f} seconds")
print(f"Total members processed: {len(set(known_face_names))}")
print(f"Total unique encodings: {len(known_face_encodings)}")
