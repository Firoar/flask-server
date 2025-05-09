import cv2
import os
from datetime import datetime
import time

CAPTURED_DIR = os.path.join("data", "captured")

def capture_images(num_images=5, delay=2):
    if not os.path.exists(CAPTURED_DIR):
        os.makedirs(CAPTURED_DIR)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return []  # Return early if camera cannot be opened

    print("📷 Camera opened successfully.")

    captured_files = []
    for i in range(num_images):
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Failed to capture image {i + 1}")
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"image_{timestamp}.jpg"
        file_path = os.path.join(CAPTURED_DIR, filename)

        if cv2.imwrite(file_path, frame):
            print(f"✅ Image {i + 1} saved: {file_path}")
            captured_files.append(file_path)
        else:
            print(f"❌ Failed to save image {i + 1}")

        time.sleep(delay)

    cap.release()
    return captured_files
