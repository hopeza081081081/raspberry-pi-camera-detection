#!/bin/sh
cd /home/pi/raspberry-pi-camera-detection

nohup ./run.sh > ./camera_startup.log 2>&1 &
exit 0