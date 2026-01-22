# Raspberry Pi Classroom Person Detection

This project detects people in a classroom using a Raspberry Pi 4 and a Camera, and publishes the status via MQTT.

## Prerequisites

- Raspberry Pi 4
- Pi Camera or USB Webcam
- Raspberry Pi 4
- Pi Camera or USB Webcam
- **Python 3.7 - 3.11** 
  - *Python 3.7.3 (Legacy Pi OS) is supported! (I have adjusted dependencies for it)*
  - *Python 3.9 - 3.11 is recommended.*
- Internet connection (for initial setup)
- Internet connection (for initial setup)

## Installation

## Quick Start (Recommended)

I have included a script `run.sh` that automatically sets up the environment and runs the program.

1.  **Run the helper script**:
    ```bash
    ./run.sh
    ```
    *This script will:*
    *   Create a virtual environment (`venv`) if it doesn't exist.
    *   Install all dependencies.
    *   Download the model files.
    *   Start the detection program.

## Manual Installation

If you prefer to set it up manually:

1.  **Create & Activate Virtual Environment**:
    ```bash
    python3 -m venv raspberry-pi-camera-detection
    source raspberry-pi-camera-detection/bin/activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download Models**:
    ```bash
    python download_models.py
    ```
4.  **Run**:
    ```bash
    python main.py
    ```

- The script will output "Person detected" and publish to MQTT.
- Press `q` to exit detection loop (if a window is shown).

## Configuration

Edit `config.py` to change settings:
```python
# MQTT
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "classroom/detection"

# Detection
CONFIDENCE_THRESHOLD = 0.5
TARGET_LABELS = ["person"]
```

## MQTT Payload

The device publishes JSON data to `classroom/detection`:
```json
{
  "status": "occupied",
  "count": 2,
  "timestamp": 1715678900.123
}
```
- `status`: "occupied" or "empty"
- `count`: Number of people detected
