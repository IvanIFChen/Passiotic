import React, { Component } from 'react';
import './App.css';
import Counter from './components/counter';
import Chart from './components/chart';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeDeviceCount: null,
      deviceList: null,
      fetchActiveDevicesIntervalId: null
    };
  }

  componentWillMount() {
    const fetchActiveDevices = async () => {
      const req = new Request(
        'https://06apquhqjg.execute-api.us-east-1.amazonaws.com/prod/api'
      );
      const res = await fetch(req);

      if (res.status !== 200) {
        console.error('Could not fetch active devices');
        return;
      }

      const data = await res.json();
      const items = data.Items;

      let latestDate;
      items.forEach(item => {
        const endDateTime = Date.parse(item.end_time);
        if (endDateTime > latestDate || latestDate === undefined) {
          latestDate = endDateTime;
        }
      });

      const activeDeviceCount = items.filter(
        item => Date.parse(item.end_time) === latestDate
      ).length;

      this.setState({
        activeDeviceCount: activeDeviceCount,
        deviceList: items
      });
    };

    if (!this.state.fetchActiveDevicesIntervalId) {
      const id = setInterval(fetchActiveDevices, 5000);
      this.setState({
        fetchActiveDevicesIntervalId: id
      });
    }
  }

  componentWillUnmount() {
    clearInterval(this.state.fetchActiveDevicesIntervalId);
  }

  render() {
    return (
      <div className="App">
        <Counter count={this.state.activeDeviceCount} />
        <br />
        <Chart activeDevices={this.state.activeDevices} />
      </div>
    );
  }
}

export default App;
