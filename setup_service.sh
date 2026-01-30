#!/bin/bash

# Configuration
SERVICE_NAME="camera-detection"
USER_NAME=$USER
# Get absolute path of the directory containing this script
WORK_DIR=$(pwd)
EXEC_CMD="$WORK_DIR/run.sh"

echo "Installing $SERVICE_NAME service..."
echo "  User: $USER_NAME"
echo "  Directory: $WORK_DIR"
echo "  Command: $EXEC_CMD"

# Create Service File
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Raspberry Pi Camera Person Detection
After=network.target

[Service]
ExecStart=$EXEC_CMD
WorkingDirectory=$WORK_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
RestartSec=10
User=$USER_NAME
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Reload and Enable
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
echo "Enabling service to start on boot..."
sudo systemctl enable $SERVICE_NAME
echo "Starting service now..."
sudo systemctl start $SERVICE_NAME

echo "---------------------------------------------------"
echo "Done! Service is running."
echo "Check status: sudo systemctl status $SERVICE_NAME"
echo "View logs:    journalctl -u $SERVICE_NAME -f"
echo "Stop service: sudo systemctl stop $SERVICE_NAME"
echo "---------------------------------------------------"
