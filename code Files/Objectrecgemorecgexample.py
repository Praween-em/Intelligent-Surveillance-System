import cv2
import numpy as np
import cvlib as cv
from cvlib.object_detection import draw_bbox
from deepface import DeepFace
import telebot
import threading
import os
import tkinter as tk

exit_event = threading.Event()

def send_telegram_notification(image_path):
    # Initialize Telegram bot with your bot token
    bot = telebot.TeleBot(token='YOUR_TELEGRAM_BOT_TOKEN')
    
    # Load image
    photo = open(image_path, 'rb')
    
    # Send photo to the desired Telegram account
    bot.send_photo(chat_id='YOUR_TELEGRAM_CHAT_ID', photo=photo)
    
    # Close the image file
    photo.close()

def object_detection():
    while not exit_event.is_set():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting...")
            break
        
        bbox, label, conf = cv.detect_common_objects(frame)
        frame = draw_bbox(frame, bbox, label, conf)
        cv2.imshow('Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def emotion_recognition():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while not exit_event.is_set():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting...")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analyze['dominant_emotion']
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            frame = cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.imshow('Emotion Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def object_detection_and_recognition():
    while not exit_event.is_set():
        img_resp = cv2.VideoCapture(0)
        ret, frame = img_resp.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting...")
            break
        
        frame = object_detection(frame)
        frame = emotion_recognition(frame)
        
        cv2.imshow('Object Detection and Emotion Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Send Telegram notification only during live stream
        img_name = 'alert_image.jpg'
        cv2.imwrite(img_name, frame)
        send_telegram_notification(img_name)

    cv2.destroyAllWindows()

def open_operation_window():
    operation_window = tk.Toplevel()
    operation_window.title("Operation Selection")
    operation_window.geometry("200x200")

    # Create two buttons for detection and recognition
    detection_button = tk.Button(operation_window, text="Detection", command=perform_detection)
    detection_button.pack(pady=10)

    recognition_button = tk.Button(operation_window, text="Recognition", command=perform_recognition)
    recognition_button.pack(pady=10)

def play_stream():
    t = threading.Thread(target=object_detection_and_recognition)
    t.start()

def perform_detection():
    t = threading.Thread(target=object_detection)
    t.start()

def perform_recognition():
    t = threading.Thread(target=emotion_recognition)
    t.start()

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Intelligent Surveillance System")

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the desired width and height for the window (70% of the screen size)
    window_width = int(0.7 * screen_width)
    window_height = int(0.7 * screen_height)

    # Position the window in the center of the screen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window size and position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Set the background color of the title
    title_background_color = "blue"

    # Create a label at the top of the window with custom styling
    title_label = tk.Label(root, text="Intelligent Surveillance System", bg=title_background_color, fg="white", font=("Helvetica", 24))
    title_label.pack(fill=tk.BOTH)

    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Create a button to start the stream
    select_button = tk.Button(button_frame, text="Select", command=open_operation_window)
    select_button.grid(row=0, column=0, padx=5)

    # Create a button for live stream
    live_stream_button = tk.Button(button_frame, text="Live Stream", command=play_stream)
    live_stream_button.grid(row=1, column=0, padx=5)

    # Run the event loop
    root.mainloop()

if __name__ == '__main__':
    print("Starting object detection and emotion recognition...")
    main()
http://192.168.29.51/cam-hi.jpg'