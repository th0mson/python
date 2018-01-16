#!/bin/bash

WEBMON_DIR="/opt/webmon"

sudo apt-get update
sudo apt-get install python python-pip
sudo pip install --upgrade pip
sudo -H pip install requests

echo "Creating directory"
echo "-----------------------"
if [ ! -d ${WEBMON_DIR} ]; then
    echo "Creating dir for script"
    sudo mkdir ${WEBMON_DIR}
    echo "-----------------------"
fi

echo "Copy scripts"
echo "-----------------------"
sudo cp *.py ${WEBMON_DIR}/
sudo cp *.json ${WEBMON_DIR}/
sudo cp webmon.service /etc/systemd/system/webmon.service

sudo sed -i "s|;WorkingDirectory=|WorkingDirectory=${WEBMON_DIR}|g" /etc/systemd/system/webmon.service

sudo systemctl enable webmon.service
