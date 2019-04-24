import React from 'react';
import { Line } from 'react-chartjs-2';

const ChartComponent = props => {
  return (
    <Line
      data={{
        labels: ['1', '2', '3', '4'],
        datasets: [
          {
            label: 'Hi',
            data: [20, 30, 50, 10]
          }
        ]
      }}
      height={100}
      width={200}
    />
  );
};

export default ChartComponent;
