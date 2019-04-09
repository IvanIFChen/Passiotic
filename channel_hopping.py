import threading
import subprocess
import time


class ChannelHopper(threading.Thread):
    """
    A thread worker that hops between an array of channels in order every n seconds.
    """

    def __init__(self, channels, interval, interface):
        """
        channels -- An array of integers representing the channels to hop between.
        frequency -- The number of seconds between each hop.
        interface -- The wireless interface to switch.
        """
        super().__init__()
        self.channels = channels
        self.interval = interval
        self.stop = threading.Event()
        self.interface = interface

    def run(self):
        chan_index = 0
        while not self.stop.isSet():
            chan_integer = self.channels[chan_index]
            chan_string = str(
                chan_integer) if chan_integer > 9 else '0' + str(chan_integer)

            subprocess.run(
                ['iwconfig', self.interface, 'channel', chan_string])

            print('Current channel is {}'.format(chan_string))

            chan_index = (chan_index + 1) % len(self.channels)

            time.sleep(self.interval)

    def join(self, timeout=None):
        self.stop.set()
        super().join(timeout)
