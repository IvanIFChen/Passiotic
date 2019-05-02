import matplotlib.pyplot as plt
import json
from dateutil import parser
from pprint import pprint
from collections import defaultdict
from datetime import datetime, timedelta

# redacted
IVAN_MAC = 'XX:XX:XX:XX:XX:XX'
ROOMMATE1_MAC = 'XX:XX:XX:XX:XX:XX'
ROOMMATE2_MAC = 'XX:XX:XX:XX:XX:XX'
ROOMMATE3_MAC = 'XX:XX:XX:XX:XX:XX'


def load_from_file(filename):
    data = defaultdict(list)
    raw_data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            x = json.loads(line)
            round_id = x['round_id']['n']
            pi = x['pi_id']['s']
            mac = x['device_mac']['s']
            raw_data.append((round_id, mac))
    for d in raw_data:
        data[d[0]] += [d[1]]

    return data


if __name__ == '__main__':
    data = load_from_file('dynamo_exports/ivan_home_weekend_test')
    keys = sorted(data.keys(), key=lambda x: int(x))
    data = [(key, data[key]) for key in keys]
    f, ax = plt.subplots(1)
    is_in = lambda who, l: 1 if who in l else 0
    ydata_ivan = [is_in(IVAN_MAC, x[1]) for x in data]
    ydata_rommmate1 = [is_in(ROOMMATE1_MAC, x[1]) for x in data]
    ydata_roommate2 = [is_in(ROOMMATE2_MAC, x[1]) for x in data]
    ydata_roommate3 = [is_in(ROOMMATE3_MAC, x[1]) for x in data]
    xdata = [x[0] for x in data]
    ax.plot(xdata, ydata_ivan, label='me')
    ax.plot(xdata, ydata_rommmate1, label='roommate 1')
    ax.plot(xdata, ydata_roommate2, label='roommate 2')
    ax.plot(xdata, ydata_roommate3, label='roommate 3')
    ax.set_ylim(bottom=0, top=3)

    plt.legend()
    plt.show()
