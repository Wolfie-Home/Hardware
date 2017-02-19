#!/bin/sh

sudo apt-get update
sudo apt-get upgrade

# install mosquitto
sudo apt-get dist-upgrade
sudo apt-get install mosquitto mosquitto-clients python-mosquitto
sudo pip install paho-mqtt
