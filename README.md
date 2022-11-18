## Two factor authentication system with raspberrypi, camera, and RFID reader using face recognition.
The system works with mongodb database that can be on another server or on localhost. Two raspberry pis are used: one for doing the main tasks of authentication and registration, and an another raspberry pi for a Telegram chat-bot that sends messages to subscribed users through Telegram on login attempts and stores the logs in a mongodb database.  
### Setup of RPI 1:
```
sudo install python3
sudo apt-get install python3-pip
pip3 install opencv-python
pip3 install face_recognition
pip3 install paho-mqtt
```
### Setup of RPI 2:
```
sudo install python3
sudo apt-get install python3-pip
pip3 install paho-mqtt
pip3 install python-telegram-bot



