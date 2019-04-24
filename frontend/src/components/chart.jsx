import React from 'react';
import { Line } from 'react-chartjs-2';
import { getLatestRoundForPi, getItemsForPiRound } from '../utils';

const ChartComponent = props => {
  const maxRounds = new Map();
  props.piIds.forEach(pi => {
    maxRounds.set(pi, getLatestRoundForPi(pi, props.items));
  });

  const minRounds = new Map();
  for (let round of maxRounds) {
    if (round[1] <= props.maxRound) {
      minRounds.set(round[0], 0);
    } else {
      minRounds.set(round[0], round[1] - props.maxRound);
    }
  }

  const itemsPerSlot = new Array(props.maxRound).fill([]);
  props.piIds.forEach(pi => {
    for (let i = minRounds.get(pi); i <= maxRounds.get(pi); i++) {
      let items = getItemsForPiRound(pi, i, props.items);
      itemsPerSlot[i % props.maxRound] = itemsPerSlot[
        i % props.maxRound
      ].concat(items);
    }
  });

  const counts = [];
  itemsPerSlot.forEach(items => {
    const deviceSet = new Set();
    items.forEach(item => {
      deviceSet.add(item.device_mac);
    });

    if (deviceSet.size !== 0) {
      counts.push(deviceSet.size);
    }
  });

  const labels = [];
  for (let i = 1; i < counts.length; i++) {
    labels.push('Report ' + i.toString());
  }

  return (
    <Line
      data={{
        labels,
        datasets: [
          {
            label: 'Number of Devices',
            data: counts,
            borderColor: '#8e5ea2',
            fill: false
          }
        ]
      }}
      height={100}
      width={200}
    />
  );
};

export default ChartComponent;
