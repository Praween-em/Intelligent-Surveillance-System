---

# **Intelligent Surveillance System (ISS)**  
Enhancing security and safety through real-time monitoring, object recognition, and emotion detection.

---

## **Overview**  
The Intelligent Surveillance System (ISS) leverages IoT, computer vision, and deep learning to revolutionize traditional surveillance methods. By integrating hardware and software solutions, the ISS enables real-time monitoring, threat detection, and alert generation, addressing critical security challenges in various environments like public spaces, industrial facilities, and private establishments.

---

## **Features**  
- **Automated Monitoring:** Reduces reliance on manual surveillance.
- **Real-Time Threat Detection:** Uses AI for instant recognition of potential threats.
- **Emotion Detection:** Analyzes facial expressions to gauge emotional states.
- **Alerts System:** Sends notifications via Telegram upon detecting threats.
- **Advanced Analytics:** Offers deep insights into monitored activities.

---

## **System Architecture**  
The ISS employs a modular and scalable architecture to ensure reliability and performance:

### 1. **Hardware Components**
- **Arduino Uno:** Acts as a control unit for the sensors.
- **ESP32-CAM:** Captures real-time video and transmits it over WiFi.  
- **Sensors (Optional):** Motion or thermal sensors can enhance detection accuracy.

### 2. **Software Components**
- **YOLO (You Only Look Once):** For object detection.  
- **DeepFace Module:** For facial recognition and emotion analysis.
- **Telegram API:** For sending real-time alerts to a specified group.

### 3. **Communication**
- **HTTPS Protocol:** Ensures secure data transmission to the server.
- **Client-Server Model:** Enhances fault tolerance and system performance.

---

## **Project Structure**  
The repository is organized as follows:

```
Intelligent-Surveillance-System/
│
├── hardware/
│   ├── arduino_code/           # Scripts for Arduino Uno
│   ├── esp32_cam_code/         # Scripts for ESP32-CAM setup
│
├── software/
│   ├── object_detection/       # YOLO model and configuration
│   ├── emotion_detection/      # DeepFace modules and scripts
│   ├── alerts/                 # Telegram API integration
│   ├── ui/                     # User Interface code
│
├── tests/
│   ├── unit_tests/             # Unit testing scripts for modules
│   ├── integration_tests/      # System-wide testing scripts
│
├── data/
│   ├── training_data/          # Sample datasets for YOLO and DeepFace
│   ├── logs/                   # Log files for debugging
│
├── docs/
│   ├── README.md               # Project documentation
│   ├── INSTALLATION.md         # Setup and installation guide
│
└── LICENSE                     # Licensing information
```

---

## **Working of the System**  
1. **Image Capture:**  
   - The ESP32-CAM captures images or video streams and sends them to the server over WiFi.  

2. **Object Detection:**  
   - The YOLO model processes the incoming images to identify objects in real-time.  

3. **Emotion Detection:**  
   - The DeepFace module analyzes facial expressions to identify emotional states.

4. **Threat Assessment and Alerting:**  
   - Detected threats trigger an immediate alert, which is sent to security personnel via Telegram.

5. **Data Logging and Analytics:**  
   - All events are logged for post-analysis, providing actionable insights into security trends.

---

## **Hardware Requirements**
- **ESP32-CAM**
- **Arduino Uno**
- **WiFi Module**
- (Optional) **Sensors:** Thermal or motion detectors.

---

## **Software Requirements**
- **Python 3.8+**
- **YOLO (v3 or higher)**: Object detection model.
- **DeepFace:** Emotion and facial recognition.
- **Telegram API:** For alert system integration.
- **Flask or Django:** Server-side framework for API and UI.
- **OpenCV:** Image processing library.

---

## **Setup Instructions**
1. **Hardware Configuration:**
   - Connect the ESP32-CAM and Arduino Uno as per the wiring diagram in `/docs/hardware_setup.pdf`.

2. **Software Installation:**
   - Install the required Python packages:  
     ```bash
     pip install -r requirements.txt
     ```
   - Upload the Arduino and ESP32-CAM scripts from the `/hardware` directory.

3. **Run the System:**
   - Start the server:  
     ```bash
     python app.py
     ```
   - Access the User Interface at `http://<server-ip>:5000`.

---

## **Testing**
- Unit and integration tests are located in the `/tests` directory.
- Run all tests using:  
  ```bash
  pytest
  ```

---

## **Future Enhancements**
- **Edge Computing Integration:** Reduce latency by processing data closer to the source.
- **Multi-Sensor Fusion:** Integrate thermal and motion sensors for better detection.
- **Mobile App:** Develop a cross-platform app for remote monitoring.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
