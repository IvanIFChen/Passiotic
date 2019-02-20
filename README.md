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

### Notes for running the script
Make sure to change the `INTERFACE` field to appropriate device name. E.g. mac is usually `en0` and on a Pi is `wlan0`.

## Current issue trying to run on Pi
* Permission issue (need sudo to start tshark in monitor mode)
  - workaround by running it in root
* Not capturing packets
  - "Listening..." showed up, no error, was not able to capture the association request packets.
  - looks like Pi's default card does not support monitor mode, see [this](https://www.reddit.com/r/raspberry_pi/comments/5m8u29/how_do_i_enable_monitor_mode_on_my_rpi_3b_wifi/)
