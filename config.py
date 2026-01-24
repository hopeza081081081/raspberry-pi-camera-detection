# MQTT Configuration
# MQTT Configuration
MQTT_BROKER = "10.10.200.70"
MQTT_PORT = 1883
MQTT_TOPIC = "myFinalProject/rpi2/objDetector"
MQTT_TOPIC_LWT = "myFinalProject/rpi2/onlineStatus/online"
MQTT_USERNAME = "admin"
MQTT_PASSWORD = "5617091"
CLIENT_ID = "pi_classroom_detector"

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5 # 0.1 to 1.0
TARGET_LABELS = ["person"] # List of labels to detect

# Performance Settings
HEADLESS_MODE = False # Set to False if you have a monitor connected and want to see the video
NUM_THREADS = 4 # Number of threads for TFLite inference (4 is good for Pi 4)
