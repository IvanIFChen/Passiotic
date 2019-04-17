import React, { useEffect } from 'react';
import styled from '@emotion/styled';
import Chart from 'chart.js';

const ChartComponent = props => {
  const chartRef = React.createRef();
  const StyledCanvas = styled.canvas`
    width: 300px;
    height: 300px;
  `;
  useEffect(() => {
    const lineChart = new Chart(chartRef.current, {
      type: 'line',
      data: [40, 50, 20]
    });
  });
  return <StyledCanvas ref={chartRef} />;
};

export default ChartComponent;
