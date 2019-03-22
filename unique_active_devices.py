import pyshark
import logging
import subprocess
import time
from pprint import pprint

INTERFACE = 'wlan1'
MAX_CHANNEL = 11
TICK = 1  # in seconds


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


if __name__ == '__main__':
    logger = setup_log()

    cap = pyshark.LiveCapture(interface=INTERFACE, monitor_mode=True)

    print('Listening...')

    try:
        active_devices = set([])
        before = time.time()
        current_channel = 1

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
                        current_channel = current_channel + 1 if current_channel < MAX_CHANNEL else 1

                        channel_string = '0' + \
                            str(current_channel) if current_channel < 10 else str(
                                current_channel)
                        subprocess.run(
                            ['iwconfig', INTERFACE, 'channel', channel_string])
                        print('Current channel is {}'.format(current_channel))

                        # clean up addresses
                        def ignore_invalid(
                            x): return x is not None and x != 'ff:ff:ff:ff:ff:ff'
                        active_devices = {
                            x
                            for x in active_devices if ignore_invalid(x)
                        }

                        out_msg = 'Active devices: {}'.format(active_devices)
                        print(out_msg)
                        logger.debug(out_msg)

                        before = time.time()
                        active_devices = set([])

            except (AttributeError, TypeError) as e:
                print('ERROR: {}'.format(e))
                logger.debug(e)
                logger.debug(p)
                continue
    except KeyboardInterrupt:
        print('BYE')
        pass
