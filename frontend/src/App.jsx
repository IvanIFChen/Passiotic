import React, { Component } from 'react';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      active_devices: new Set(),
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

      const macAddr = data.body.Items.map(r => r.active_device_id);
      this.setState({
        active_devices: new Set(macAddr)
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
    return <div className="App" />;
  }
}

export default App;
