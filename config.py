# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "classroom/detection"
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
CLIENT_ID = "pi_classroom_detector"

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5 # 0.1 to 1.0
TARGET_LABELS = ["person"] # List of labels to detect

# Performance Settings
HEADLESS_MODE = False # Set to False if you have a monitor connected and want to see the video
NUM_THREADS = 4 # Number of threads for TFLite inference (4 is good for Pi 4)
