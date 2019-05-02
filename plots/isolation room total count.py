import matplotlib.pyplot as plt
import json
from dateutil import parser
from pprint import pprint
from collections import defaultdict
from datetime import datetime, timedelta


def load_from_file(filename):
    data = defaultdict(list)
    raw_data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            x = json.loads(line)
            round_id = x['round_id']['n']
            pi = x['pi_id']['s']
            mac = x['device_mac']['s']
            raw_data.append((round_id, pi, mac))
    for d in raw_data:
        data[d[0]] += [d[2]]
    return data


if __name__ == '__main__':
    data = load_from_file('dynamo_exports/Isolation-Room-1')
    data = sorted([(key, data[key]) for key in data.keys()],
                  key=lambda x: x[0][0])
    f, ax = plt.subplots(1)
    ydata1 = [len(x[1]) for x in data]
    xdata1 = ['round {}'.format(x[0][0]) for x in data]
    ax.plot(xdata1, ydata1, label='total devices')
    ax.set_ylim(bottom=0, top=100)

    for i, j in zip(xdata1, ydata1):
        ax.annotate(str(j), xy=((i, j + 3)))

    plt.legend()
    plt.show()
