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
            round_id = x['round_id']['n']
            pi = x['pi_id']['s']
            raw_data.append((round_id, pi))
    for d in raw_data:
        data[d] += 1
    return data


if __name__ == '__main__':
    data = load_from_file('dynamo_exports/Second-Test-Snell-2nd-Floor')
    data = sorted([(key, data[key]) for key in data.keys()],
                  key=lambda x: x[0][0])[:-1]
    pprint(data)
    f, ax = plt.subplots(1)
    ydata1 = [x[1] for x in data if x[0][1] == 'pi_1']
    ydata2 = [x[1] for x in data if x[0][1] == 'pi_2']
    xdata1 = [
        'round {}'.format(str(x[0][0])) for x in data if x[0][1] == 'pi_1'
    ]
    ax.plot(xdata1, ydata1, label='pi_1')
    ax.plot(xdata1, ydata2, label='pi_2')
    ax.set_ylim(bottom=0, top=100)

    plt.legend()
    plt.show()
