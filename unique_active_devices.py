import pyshark
import requests
import logging
import subprocess
import time
import json
from pprint import pprint
from datetime import datetime

from channel_hopping import ChannelHopper

INTERFACE = 'wlan1'
MAX_CHANNEL = 11
TICK = 60  # in seconds
CHANNEL_HOP_FREQ = 10
CHANNELS = [1, 6, 11]
PI_ID = "pi_1"
REMOTE_URL = 'https://06apquhqjg.execute-api.us-east-1.amazonaws.com/prod/api'


def setup_log():
    logging.basicConfig(
        filename='unique_active_devices.log',
        filemode="a+",
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S')

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(__name__)
    return logger


def send_active_devices(devices, logger):
    payload = {
        'active_devices': list(devices),
        'pi_id': PI_ID,
        'start_time': 'n/a',
        'end_time': str(datetime.now())
    }

    r = requests.post(REMOTE_URL, json=json.dumps(payload))

    if not (r.status_code == 200):
        logger.debug(
            'Got %s when trying to send results to central server' % r.status_code)


if __name__ == '__main__':
    logger = setup_log()

    cap = pyshark.LiveCapture(interface=INTERFACE, monitor_mode=True)

    print('Listening...')

    channel_hopper = ChannelHopper(CHANNELS, CHANNEL_HOP_FREQ, INTERFACE)
    channel_hopper.start()

    try:
        active_devices = set([])
        before = time.time()

        # for p in cap:
        for p in cap.sniff_continuously():

            try:
                # this is a DATA TYPE frame
                accept = int(p.wlan.fc_type) == 2

                if accept and p.highest_layer != '_WS.MALFORMED':
                    # TODO: clean this up
                    # Different DATA type frames have a different structure,
                    # based on observation, it could have 'sa' or 'addr'. If one them
                    # does not exist we'll append a 'None', but we'll filter that out later.
                    active_devices.add(p.wlan.get('sa'))
                    active_devices.add(p.wlan.get('addr'))

                    if time.time() - before >= TICK:
                        # clean up addresses
                        def ignore_invalid(
                            x): return x is not None and x != 'ff:ff:ff:ff:ff:ff'
                        active_devices = {
                            x
                            for x in active_devices if ignore_invalid(x)
                        }

                        out_msg = 'Active devices: {}'.format(active_devices)
                        print(out_msg)

                        send_active_devices(active_devices, logger)

                        logger.debug(out_msg, logger)

                        before = time.time()
                        active_devices = set([])

            except (AttributeError, TypeError) as e:
                print('ERROR: {}'.format(e))
                logger.debug(e)
                logger.debug(p)
                continue
    except KeyboardInterrupt:
        channel_hopper.join()
        print('BYE')
        pass
