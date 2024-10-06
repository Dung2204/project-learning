import cv2
import os
from datetime import datetime
import time

# Initialize the camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Set width
cam.set(4, 480)  # Set height

# Load the pre-trained face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if face_detector.empty():
    print("Error loading face detector.")
    cam.release()
    cv2.destroyAllWindows()
    exit()

# Define the path to the 'dataset' directory
dataset_dir = r'C:\Users\Dell\OneDrive\Pictures\Documents\Code\python\OpenCV\Project\Face recognition\Dataset'

# Ensure 'dataset' directory exists
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

count = 0
last_saved_time = time.time()
save_interval = 5  # Time interval in seconds between saving images
max_images = 30    # Maximum number of images to save  , 30 ảnh kh là tràn bộ nhớ

print("Press 'Esc' to exit and save images of faces.")

while count < max_images:
    ret, img = cam.read()
    
    if not ret:
        print("Failed to grab frame.")
        break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        print(f"Detected {len(faces)} face(s)")

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Save the images at specified intervals
    current_time = time.time()
    if current_time - last_saved_time > save_interval:
        for (x, y, w, h) in faces:
            face_img = img[y:y + h, x:x + w]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(dataset_dir, f"face_{timestamp}_{count}.jpg")
            if cv2.imwrite(filename, face_img):
                print(f"Image saved as {filename}")
                count += 1
                if count >= max_images:
                    break
            else:
                print(f"Failed to save image {filename}")
        
        last_saved_time = current_time
    
    cv2.imshow('Face Detection', img)

    k = cv2.waitKey(1) & 0xff
    if k == 27:  # 'Esc' key
        break

print("\nExiting...")
cam.release()
cv2.destroyAllWindows()



