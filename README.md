# Passiotic
A passive radio device ticker

## Installation
Make sure Tshark is installed, for linux:
```
sudo apt-get update
sudo apt-get install tshark
```
Make sure you are using Python 3 then setup the virtual env:
```
pip3 install virtualenv
export PATH="~/.local/bin:$PATH"
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
python main.py
```
`deactivate` to deactivate the virtual env.

## Current issue trying to run on Pi
* Permission issue (need sudo to start tshark or something?)
  - workaround by running it in root
* Not capturing packets
  - "Listening..." showed up, no error, was not able to capture the association request packets.
  - it was working on mac with "en0" interface, but changed the to "wlan0" for the Pi and it's not working, it could totally be something else tho.
