import React, { Component } from 'react';
import './App.css';
import Counter from './components/counter';
import ChartComponent from './components/chart';

const PI_IDS = ['pi_1', 'pi_2'];

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

      const piItems = new Map();
      PI_IDS.forEach(id => {
        const pi = items.filter(item => item.pi_id === id);
        piItems.set(id, pi);
      });

      const piLatestRound = new Map();
      for (let pi of piItems.keys()) {
        piLatestRound.set(pi, 0);
      }

      for (let items of piItems) {
        for (let item of items[1]) {
          if (piLatestRound.get(items[0]) < item.round_id) {
            piLatestRound.set(items[0], item.round_id);
          }
        }
      }

      const piFiltered = new Map();
      for (let pi of piItems.keys()) {
        const filteredItems = piItems
          .get(pi)
          .filter(item => item.round_id === piLatestRound.get(pi));
        piFiltered.set(pi, filteredItems);
      }

      const uniqueDevices = new Set();
      for (let items of piFiltered.values()) {
        for (let item of items) {
          uniqueDevices.add(item.device_mac);
        }
      }

      this.setState({
        activeDeviceCount: uniqueDevices.size,
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
        <ChartComponent activeDevices={this.state.activeDevices} />
      </div>
    );
  }
}

export default App;
