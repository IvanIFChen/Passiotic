import React, { Component } from 'react';
import './App.css';
import Counter from './components/counter';
import ChartComponent from './components/chart';
import { getItemsForPiRound, getLatestRoundForPi } from './utils';

const PI_IDS = ['pi_1', 'pi_2'];
const MAX_NUM_ROUNDS = 20; // The maximum number of rounds to graph

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeDeviceCount: null,
      allItems: null,
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

      const piLatestRound = new Map();
      for (let pi of PI_IDS) {
        piLatestRound.set(pi, getLatestRoundForPi(pi, items));
      }

      const piFiltered = new Map();
      for (let pi of PI_IDS) {
        const filteredItems = getItemsForPiRound(
          pi,
          piLatestRound.get(pi),
          items
        );

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
        allItems: items
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
        <ChartComponent
          activeDevices={this.state.allItems}
          maxRound={MAX_NUM_ROUNDS}
        />
      </div>
    );
  }
}

export default App;
