import requests
from uuid import getnode 

def init_id():
    try:
        # try to find the already generated node_id
        with open('node_id', 'rb') as f:
            return f.read()
    except FileNotFoundError:
        # generate a new one and store it as a file for later use
        with open('node_id', 'w') as f:
            node_id = hex(getnode())
            f.write(node_id)
            return node_id

class Api():
    API_URL = 'https://06apquhqjg.execute-api.us-east-1.amazonaws.com/prod/api'
    TEST = {
        'active_devices': ['11:22:33:44:55:66', 'AA:BB:CC:DD:EE:FF', '12:34:56:78:90:00'],
        'pi_id': '11:11:11:11:11:11',
        'start_time': '2019-04-04T13:10:50.673931-04:00',
        'end_time': '2019-04-04T13:15:50.673931-04:00'
    }

    def __init__(self):
        self.node_id = init_id()
    
    def upload_addresses(macs):
        requests.post(self.API_URL, self.TEST)

