#!/bin/bash

# Define the virtual environment directory
VENV_DIR="raspberry-pi-camera-detection"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    # Use system-site-packages to speed up install by using apt versions of numpy/opencv if available
    python3 -m venv --system-site-packages $VENV_DIR
    
    echo "Activating virtual environment..."
    source $VENV_DIR/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Downloading models..."
    python download_models.py
else
    echo "Activating virtual environment..."
    source $VENV_DIR/bin/activate
fi

# Always check/install dependencies (pip will skip if already satisfied)
echo "Checking dependencies..."
# Use PiWheels to get pre-compiled binaries (fast!) instead of compiling (slow!)
pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple

# Attempt to install TFLite Runtime (Specific for Raspberry Pi)
if ! python -c "import tflite_runtime" &> /dev/null; then
    echo "TFLite Runtime not found. Attempting to install..."
    # Try PyPI first
    pip install tflite-runtime || echo "Warning: Standard installation failed. Trying Google Coral repo..."
    
    # If standard PyPI failed or not found, try Coral Repo
    if ! python -c "import tflite_runtime" &> /dev/null; then
         pip install tflite-runtime --extra-index-url https://google-coral.github.io/py-repo/ || echo "Warning: TFLite installation failed. Usage will fallback to Simulation Mode."
    fi
fi

# Run the main application
echo "Starting Person Detection..."
python main.py
