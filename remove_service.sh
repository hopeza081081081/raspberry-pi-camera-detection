#!/bin/bash

SERVICE_NAME="camera-detection"

echo "Removing $SERVICE_NAME service..."

# Stop the service
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "Stopping service..."
    sudo systemctl stop $SERVICE_NAME
fi

# Disable the service
if systemctl is-enabled --quiet $SERVICE_NAME; then
    echo "Disabling service..."
    sudo systemctl disable $SERVICE_NAME
fi

# Remove the service file
if [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
    echo "Removing service file..."
    sudo rm "/etc/systemd/system/$SERVICE_NAME.service"
fi

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "---------------------------------------------------"
echo "Done! Service '$SERVICE_NAME' has been removed."
echo "---------------------------------------------------"
