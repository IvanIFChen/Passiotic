import pyshark
import logging

def setup_log():
    logging.basicConfig(filename='main.log', filemode="a+", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    console = logging.StreamHandler()  
    console.setLevel(logging.ERROR)  
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(__name__)
    return logger

if __name__ == '__main__':
    logger = setup_log()

    # cap = pyshark.FileCapture('pcaps/tuna8-join-ddwrt.pcap', display_filter='wlan.sa[4:]==8f:28 and wlan.fc.type==0')
    cap = pyshark.LiveCapture(interface='wlan0', monitor_mode=True, display_filter='wlan.fc.type==0')

    print('Listening...')

    # for p in cap:
    for p in cap.sniff_continuously():
        is_asso_req = int(p.wlan.fc_type_subtype) == 0
        # safety check, should always be true since we have display filter on
        if is_asso_req:
            try:
                ssid = p.layers[3].ssid
                src_addr = p.wlan.sa
                dest_addr = p.wlan.da
                msg = 'Device \"{}\" is trying to join \"{}\"'.format(src_addr, ssid)
                print(msg)
                logger.debug(msg)
            except AttributeError as e:
                print(e)
                continue
