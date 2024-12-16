import cv2
import numpy as np
from cvlib.object_detection import detect_common_objects, draw_bbox
from deepface import DeepFace
import telebot
import threading
import tkinter as tk

exit_event = threading.Event()

def send_telegram_notification(image_path):
    try:
        bot = telebot.TeleBot(token='7076359119:AAGux-Up7BZ-JrO9SnqBpH1uo4GcOYqBjr8')
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id='-4264411724', photo=photo)
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")

def object_detection():
    cap = cv2.VideoCapture(0)
    while not exit_event.is_set():
        ret, frame = cap.read()
        if ret:
            bbox, label, conf = detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf)
            cv2.imshow('Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def emotion_recognition():
    cap = cv2.VideoCapture(0)
    while not exit_event.is_set():
        ret, frame = cap.read()
        if ret:
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(analyze, list) and len(analyze) > 0:
                analyze = analyze[0]
            emotion = analyze['dominant_emotion']
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Emotion Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def object_detection_and_recognition():
    cap = cv2.VideoCapture(0)
    while not exit_event.is_set():
        ret, frame = cap.read()
        if ret:
            bbox, label, conf = detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf)
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(analyze, list) and len(analyze) > 0:
                analyze = analyze[0]
            emotion = analyze['dominant_emotion']
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            dangerous_emotions = {'angry', 'sad', 'unhappy', 'neutral'}
            dangerous_objects = {'knife', 'gun' , 'glass botctle' , 'iron rod', 'stick'}  # Add more dangerous objects if needed
            if emotion in dangerous_emotions and any(obj in dangerous_objects for obj in label):
                img_name = 'alert_image.jpg'
                cv2.imwrite(img_name, frame)
                send_telegram_notification(img_name)
            cv2.imshow('Object Detection and Emotion Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.start()
    return thread

def open_operation_window():
    operation_window = tk.Toplevel(root)
    operation_window.title("Operations")
    recognition_button = tk.Button(operation_window, text="Recognition", command=lambda: start_thread(emotion_recognition))
    recognition_button.pack(pady=10)
    detection_button = tk.Button(operation_window, text="Detection", command=lambda: start_thread(object_detection))
    detection_button.pack(pady=10)
    detection_and_recognition_button = tk.Button(operation_window, text="Alert System", command=lambda: start_thread(object_detection_and_recognition))
    detection_and_recognition_button.pack(pady=10)

def start_button_click():
    open_operation_window()

def main():
    global root
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
    start_button = tk.Button(root, text="Start", command=start_button_click)
    start_button.pack(pady=10)
    root.mainloop()

if __name__ == '__main__':
    print("Starting object detection and emotion recognition...")
    main()
