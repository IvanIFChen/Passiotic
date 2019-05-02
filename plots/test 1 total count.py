import matplotlib.pyplot as plt
import json
from dateutil import parser
from pprint import pprint
from collections import defaultdict
from datetime import datetime, timedelta


def load_from_file(filename):
    data = defaultdict(int)
    raw_data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            x = json.loads(line)
            date = parser.parse(x['end_time']['s'])
            pi = x['pi_id']['s']
            if pi == 'pi_2':
                date = date - timedelta(minutes=6)
            raw_data.append(date.minute)
    for d in raw_data:
        data[d] += 1
    return data


if __name__ == '__main__':
    data = load_from_file('dynamo_exports/First-Test-Snell-2nd-Floor')
    data = [(key, data[key]) for key in data.keys()]
    data.sort(key=lambda x: x[0])
    f, ax = plt.subplots(1)
    ydata = [x[1] for x in data]
    xdata = ['11:{} AM'.format(x[0]) for x in data]
    ax.plot(xdata, ydata, label='total devices')
    ax.set_ylim(bottom=0, top=100)
    plt.legend()
    plt.show()
