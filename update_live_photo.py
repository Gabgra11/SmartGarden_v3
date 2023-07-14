import os
import requests
import cv2
from datetime import datetime
from scripts import db

# Check if the required environment variables are set
if "IMGUR_CLIENT_ID" not in os.environ or "IMGUR_CLIENT_SECRET" not in os.environ:
    print("Please set the 'IMGUR_CLIENT_ID' and 'IMGUR_CLIENT_SECRET' environment variables.")
    exit(1)

# Create a folder to store the images
image_folder = "captured_images"
os.makedirs(image_folder, exist_ok=True)

# Capture image from webcam
def capture_image():
    camera = cv2.VideoCapture(0)
    _, frame = camera.read()
    camera.release()
    return frame

# Save image to file
def save_image(image):
    now = datetime.now()
    filename = f"webcam_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = os.path.join(image_folder, filename)
    cv2.imwrite(file_path, image)
    return file_path

# Upload image to Imgur
def upload_to_imgur(image_path):
    client_id = os.environ["IMGUR_CLIENT_ID"]
    client_secret = os.environ["IMGUR_CLIENT_SECRET"]
    url = "https://api.imgur.com/3/image"

    headers = {
        "Authorization": f"Client-ID {client_id}"
    }

    with open(image_path, "rb") as file:
        files = {"image": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["id"]

    return None

# Main execution
if __name__ == "__main__":
    # Capture image
    image = capture_image()

    # Save image
    image_path = save_image(image)
    print(f"Image saved: {image_path}")

    # Upload image to Imgur
    imgur_id = upload_to_imgur(image_path)
    if imgur_id:
        print(f"Image uploaded to Imgur: {imgur_id}")
    else:
        print("Failed to upload image to Imgur.")
    
    # Upload URL to DB:
    db.add_image_id(imgur_id)
