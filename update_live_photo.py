import os
import requests
import cv2
from datetime import datetime
from scripts import db
import time

def capture_image():
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    camera.release()
    return frame

def save_image(image):
    # Create images folder if not present:
    image_folder = "captured_images"
    os.makedirs(image_folder, exist_ok=True)
    now = datetime.now()
    filename = f"webcam_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = os.path.join(image_folder, filename)
    cv2.imwrite(file_path, image)
    return file_path

def upload_to_imgur(image_path):
    client_id = os.environ["IMGUR_CLIENT_ID"]
    client_secret = os.environ["IMGUR_CLIENT_SECRET"]
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Client-ID {client_id}"}

    with open(image_path, "rb") as file:
        files = {"image": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["id"]

    return None

if __name__ == "__main__":
    # Capture webcam image:
    image = capture_image()

    # Save image locally:
    image_path = save_image(image)
    print(f"Image saved: {image_path}")

    # Upload image to Imgur:
    imgur_id = upload_to_imgur(image_path)
    if imgur_id:
        print(f"Image uploaded to Imgur: {imgur_id}")
    else:
        print("Failed to upload image to Imgur.")
    
    # Upload Imgur ID to db:
    db.add_image_id(imgur_id)
