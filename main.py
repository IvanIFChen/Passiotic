import pyshark

# cap = pyshark.FileCapture('pcaps/tuna8-join-ddwrt.pcap', display_filter='wlan.sa[4:]==8f:28 and wlan.fc.type==0')
cap = pyshark.LiveCapture(interface='en0', monitor_mode=True, display_filter='wlan.fc.type==0')

# for p in cap:
for p in cap.sniff_continuously():
    is_asso_req = int(p.wlan.fc_type_subtype) == 0
    # safety check, should always be true since we have display filter on
    if is_asso_req:
        ssid = p.layers[3].ssid
        src_addr = p.wlan.sa
        dest_addr = p.wlan.da
        print('Device \"{}\" is trying to join \"{}\"'.format(src_addr, ssid))
