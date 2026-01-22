#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
    
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
pip install -r requirements.txt

# Run the main application
echo "Starting Person Detection..."
python main.py
