import cv2
import numpy as np
from cvlib.object_detection import detect_common_objects, draw_bbox
from deepface import DeepFace
import telebot
import threading
import urllib.request
import tkinter as tk
from urllib.parse import urlparse

exit_event = threading.Event()

def send_telegram_notification(image_path):
    bot = telebot.TeleBot(token='7076359119:AAGux-Up7BZ-JrO9SnqBpH1uo4GcOYqBjr8')
    photo = open(image_path, 'rb')
    bot.send_photo(chat_id='-4264411724', photo=photo)
    photo.close()

def validate_ip(ip_address):
    try:
        result = urlparse(ip_address)
        if result.scheme not in ['http', 'https']:
            return False
        ip_parts = result.hostname.split('.')
        if len(ip_parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_parts):
            return True
    except Exception:
        return False
    return False

def object_detection(ip_address):
    while not exit_event.is_set():
        try:
            img_resp = urllib.request.urlopen(ip_address)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            bbox, label, conf = detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf)
            cv2.imshow('Detection', frame)
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e.code} - {e.reason}")
        except Exception as e:
            print(f"Error: {e}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def emotion_recognition(ip_address):
    while not exit_event.is_set():
        try:
            img_resp = urllib.request.urlopen(ip_address)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analyze['dominant_emotion']
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                frame = cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Emotion Recognition', frame)
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e.code} - {e.reason}")
        except Exception as e:
            print(f"Error: {e}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def object_detection_and_recognition(ip_address):
    while not exit_event.is_set():
        try:
            img_resp = urllib.request.urlopen(ip_address)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            bbox, label, conf = detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf)
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analyze['dominant_emotion']
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                frame = cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Object Detection and Emotion Recognition', frame)
            img_name = 'alert_image.jpg'
            cv2.imwrite(img_name, frame)
            send_telegram_notification(img_name)
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e.code} - {e.reason}")
        except Exception as e:
            print(f"Error: {e}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def start_object_detection(ip_address):
    detection_thread = threading.Thread(target=object_detection, args=(ip_address,))
    detection_thread.start()

def start_emotion_recognition(ip_address):
    recognition_thread = threading.Thread(target=emotion_recognition, args=(ip_address,))
    recognition_thread.start()

def start_object_detection_and_recognition(ip_address):
    detection_and_recognition_thread = threading.Thread(target=object_detection_and_recognition, args=(ip_address,))
    detection_and_recognition_thread.start()

def open_operation_window():
    operation_window = tk.Toplevel(root)
    operation_window.title("Operations")
    recognition_button = tk.Button(operation_window, text="Recognition", command=lambda: start_emotion_recognition(ip_entry.get()))
    recognition_button.pack(pady=10)
    detection_button = tk.Button(operation_window, text="Detection", command=lambda: start_object_detection(ip_entry.get()))
    detection_button.pack(pady=10)
    detection_and_recognition_button = tk.Button(operation_window, text="Detection and Recognition", command=lambda: start_object_detection_and_recognition(ip_entry.get()))
    detection_and_recognition_button.pack(pady=10)

def start_button_click():
    ip_address = ip_entry.get()
    if validate_ip(ip_address):
        error_label.config(text="")
        open_operation_window()
    else:
        error_label.config(text="Invalid IP address. Please try again.")

def main():
    global ip_entry, error_label, root
    root = tk.Tk()
    root.title("Intelligent Surveillance System")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(0.7 * screen_width)
    window_height = int(0.7 * screen_height)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    title_background_color = "blue"
    title_label = tk.Label(root, text="Intelligent Surveillance System", bg=title_background_color, fg="white", font=("Helvetica", 24))
    title_label.pack(fill=tk.BOTH)
    ip_frame = tk.Frame(root)
    ip_frame.pack(pady=10)
    ip_label = tk.Label(ip_frame, text="IP Address:")
    ip_label.grid(row=0, column=0, padx=5)
    ip_entry = tk.Entry(ip_frame)
    ip_entry.grid(row=0, column=1, padx=5)
    start_button = tk.Button(ip_frame, text="Start", command=start_button_click)
    start_button.grid(row=0, column=2, padx=5)
    error_label = tk.Label(ip_frame, text="", fg="red")
    error_label.grid(row=1, column=0, columnspan=3, pady=5)
    root.mainloop()

if __name__ == '__main__':
    print("Starting object detection and emotion recognition...")
    main()
