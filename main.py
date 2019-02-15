import pyshark
import logging

INTERFACE = 'wlan0'

def setup_log():
    logging.basicConfig(filename='main.log', filemode="a+", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    console = logging.StreamHandler()  
    console.setLevel(logging.ERROR)  
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(__name__)
    return logger

if __name__ == '__main__':
    logger = setup_log()

    # DEBUG: uncomment this line to fetch from a pre-recorded file
    # cap = pyshark.FileCapture('pcaps/tuna8-join-ddwrt.pcap', display_filter='wlan.sa[4:]==8f:28 and wlan.fc.type==0')

    # DEBUG: uncomment this line to debug if the interface is able to capture packets
    cap = pyshark.LiveCapture(interface=INTERFACE)

    # DEBUG: uncomment this line to debug if monitor mode works
    # cap = pyshark.LiveCapture(interface=INTERFACE, monitor_mode=True)

    # END GOAL: uncomment this line to look for only management signals
    # cap = pyshark.LiveCapture(interface=INTERFACE, monitor_mode=True, display_filter='wlan.fc.type==0')

    print('Listening...')

    # for p in cap:
    for p in cap.sniff_continuously():

        # DEBUG: uncomment to see all packets
        # print(p)

        try:
            is_asso_req = int(p.wlan.fc_type_subtype) == 0
            if is_asso_req:
                    ssid = p.layers[3].ssid
                    src_addr = p.wlan.sa
                    dest_addr = p.wlan.da
                    msg = 'Device \"{}\" is trying to join \"{}\"'.format(src_addr, ssid)
                    print(msg)
                    logger.debug(msg)
        except (AttributeError, TypeError) as e:
            print(e)
            continue
