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
            # raw_data.append(()
            # raw_data.append(round_id)
            raw_data.append((round_id, pi, mac))
    # pprint(sorted(raw_data, key=lambda x: x[0]))
    # quit()
    for d in raw_data:
        data[d[0]] += [d[2]]

    unique_data = defaultdict(list)
    for key in data:
        unique_data[key] = list(set(data[key]))
    return data, unique_data


if __name__ == '__main__':
    data, unique_data = load_from_file(
        'dynamo_exports/Second-Test-Snell-2nd-Floor')
    unique_data = sorted(
        [(key, unique_data[key]) for key in unique_data.keys()],
        key=lambda x: x[0][0])[:-1]
    data = sorted([(key, data[key]) for key in data.keys()],
                  key=lambda x: x[0][0])[:-1]
    # pprint(data)
    # quit()
    f, ax = plt.subplots(1)
    ydata_data = [len(x[1]) for x in data]
    ydata_unique = [len(x[1]) for x in unique_data]
    xdata = ['round {}'.format(x[0]) for x in data]
    ax.plot(xdata, ydata_data, label='total devices')
    ax.plot(xdata, ydata_unique, label='unique devices')
    ax.set_ylim(bottom=0, top=100)

    for i, j in zip(xdata, ydata_data):
        ax.annotate(str(j), xy=((i, j + 3)))

    for i, j in zip(xdata, ydata_unique):
        ax.annotate(str(j), xy=((i, j + 3)))

    plt.legend()
    # plt.ylabel('Unique devices per Pi')
    plt.show()
