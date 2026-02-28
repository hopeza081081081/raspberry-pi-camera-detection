# MQTT Configuration
import uuid

def get_device_id():
    mac = uuid.getnode()
    return ''.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

# Generate unique Device ID based on MAC Address
DEVICE_ID = f"rpi_{get_device_id()}"
# Example: rpi_B827EB000000

# MQTT Configuration
MQTT_BROKER = "10.10.200.70"
MQTT_PORT = 1883
# Dynamic Topic Structure: myFinalProject/{DEVICE_ID}/objDetector
MQTT_TOPIC = f"myFinalProject/{DEVICE_ID}/objDetector"
MQTT_TOPIC_LWT = f"myFinalProject/{DEVICE_ID}/onlineStatus/online"
MQTT_USERNAME = "admin"
MQTT_PASSWORD = "5617091"
CLIENT_ID = DEVICE_ID # Client ID must be unique

# Detection Settings
CONFIDENCE_THRESHOLD = 0.3 # Increased to 0.6 because of static false positives (objects looking like people)
TARGET_LABELS = ["person"] # List of labels to detect

# Performance Settings
HEADLESS_MODE = False # Set to False if you have a monitor connected and want to see the video
NUM_THREADS = 4 # Number of threads for TFLite inference (4 is good for Pi 4, use 2-3 for Pi 3)

# Motion Verification Settings
MOTION_VERIFICATION_ENABLED = True # Complementary motion detection to reduce static false positives
MOTION_THRESHOLD = 500 # Minimum number of pixels changed to consider it "motion"
MOTION_COOLDOWN_SECONDS = 30 # Once a person is verified, keep them "active" for this long if they stay still

