# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "classroom/detection"
MQTT_USERNAME = ""
MQTT_PASSWORD = ""
CLIENT_ID = "pi_classroom_detector"

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5 # 0.1 to 1.0
TARGET_LABELS = ["person"] # List of labels to detect (e.g. "person", "cat", "dog", "laptop")
