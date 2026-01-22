
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
import json
import os
import sys
import mqtt_config
import random

# Import TFLite
TFLITE_AVAILABLE = False
try:
    import tflite_runtime.interpreter as tflite
    TFLITE_AVAILABLE = True
except ImportError:
    try:
        import tensorflow.lite as tflite
        TFLITE_AVAILABLE = True
    except ImportError:
        print("Warning: TFLite Runtime not found. Running in SIMULATION MODE.")

# Constants
MODEL_PATH = "models/detect.tflite"
LABEL_PATH = "models/coco_labels.txt"
CONFIDENCE_THRESHOLD = 0.5

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected to MQTT Broker with result code {rc}")

def load_labels(filename):
    if not os.path.exists(filename):
        return ["person", "bicycle", "car"] # Fallback defaults
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def main():
    global TFLITE_AVAILABLE
    # 1. Setup MQTT
    # Paho MQTT 2.0.0+ requires explicit CallbackAPIVersion
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_config.CLIENT_ID)
    if mqtt_config.MQTT_USERNAME and mqtt_config.MQTT_PASSWORD:
        client.username_pw_set(mqtt_config.MQTT_USERNAME, mqtt_config.MQTT_PASSWORD)
    
    client.on_connect = on_connect
    
    try:
        client.connect(mqtt_config.MQTT_BROKER, mqtt_config.MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        return

    # 2. Setup Model (if available)
    interpreter = None
    input_details = None
    output_details = None
    labels = []
    
    if TFLITE_AVAILABLE and os.path.exists(MODEL_PATH):
        try:
            interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            labels = load_labels(LABEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}. Switching to SIMULATION MODE.")
            TFLITE_AVAILABLE = False
    else:
        print("Model file not found or TFLite missing. Switching to SIMULATION MODE.")
        TFLITE_AVAILABLE = False # Force simulation

    # 3. Setup Camera
    cap = cv2.VideoCapture(0)
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Warning: Could not open camera. Will use blank frames.")

    width = 640
    height = 480
    if TFLITE_AVAILABLE and input_details:
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]

    print("Starting detection loop...")
    
    last_publish_time = 0
    PUBLISH_INTERVAL = 1.0 

    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            # Create a dummy frame if camera fails
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "No Camera - Simulation", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            time.sleep(0.1)

        people_detected = []
        person_count = 0

        if TFLITE_AVAILABLE and interpreter:
            # Real Detection Logic
            frame_resized = cv2.resize(frame, (width, height))
            input_data = np.expand_dims(frame_resized, axis=0)
            
            if input_details[0]['dtype'] == np.float32:
                input_data = (np.float32(input_data) - 127.5) / 127.5
            elif input_details[0]['dtype'] == np.uint8:
                input_data = np.uint8(input_data)

            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()

            boxes = interpreter.get_tensor(output_details[0]['index'])[0]
            classes = interpreter.get_tensor(output_details[1]['index'])[0]
            scores = interpreter.get_tensor(output_details[2]['index'])[0]

            for i in range(len(scores)):
                if scores[i] > CONFIDENCE_THRESHOLD:
                    class_id = int(classes[i])
                    label_name = labels[class_id] if class_id < len(labels) else "Unknown"
                    
                    if "person" in label_name.lower():
                        person_count += 1
                        ymin, xmin, ymax, xmax = boxes[i]
                        imH, imW, _ = frame.shape
                        (left, right, top, bottom) = (int(xmin * imW), int(xmax * imW), int(ymin * imH), int(ymax * imH))
                        
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"Person {scores[i]:.2f}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            # Simulation Logic
            # Randomly simulate "Person Detected" every ~5 seconds or based on key press
            if int(time.time()) % 10 < 5: # Detected for 5s, then Empty for 5s
                person_count = 1
                cv2.putText(frame, "SIMULATION: Person Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                person_count = 0
                cv2.putText(frame, "SIMULATION: Empty", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Publish to MQTT
        current_time = time.time()
        status = "occupied" if person_count > 0 else "empty"

        payload = {
            "status": status,
            "count": person_count,
            "timestamp": current_time,
            "mode": "simulation" if not TFLITE_AVAILABLE else "live"
        }
        
        if current_time - last_publish_time > PUBLISH_INTERVAL:
            client.publish(mqtt_config.MQTT_TOPIC, json.dumps(payload))
            print(f"Published: {payload}")
            last_publish_time = current_time

        # Show frame
        try:
            cv2.imshow('Person Detection', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        except Exception:
            # Headless environment
            pass

    cap.release()
    cv2.destroyAllWindows()
    client.loop_stop()

if __name__ == "__main__":
    main()
