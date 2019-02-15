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
