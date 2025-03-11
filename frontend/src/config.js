// Base URL for API calls
export const apiUrl = 'http://localhost:8000'; // Change this if your FastAPI backend runs on a different port

// Chart color schemes
export const chartColors = {
  system: {
    cpu: {
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
    ram: {
      borderColor: 'rgb(53, 162, 235)',
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    }
  },
  weather: {
    temp: {
      borderColor: 'rgb(255, 159, 64)',
      backgroundColor: 'rgba(255, 159, 64, 0.5)',
    }
  },
  crypto: {
    price: {
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.5)',
    }
  }
};

// External trading sites for crypto
export const tradingSites = {
  BTC: 'https://www.binance.com/en/trade/BTC_USDT',
};

// Gauge configurations
export const gaugeConfigs = {
  cpu: {
    min: 0,
    max: 100,
    arc: {
      width: 0.2,
      padding: 0.05,
      cornerRadius: 1
    },
    pointer: {
      elastic: true
    },
    colors: {
      low: '#4CAF50',  // Green
      medium: '#FFC107', // Yellow
      high: '#F44336'   // Red
    }
  },
  ram: {
    min: 0,
    max: 100,
    arc: {
      width: 0.2,
      padding: 0.05,
      cornerRadius: 1
    },
    pointer: {
      elastic: true
    },
    colors: {
      low: '#4CAF50',  // Green
      medium: '#FFC107', // Yellow
      high: '#F44336'   // Red
    }
  },
  weather: {
    min: -20,
    max: 50,
    arc: {
      width: 0.2,
      padding: 0.05,
      cornerRadius: 1
    },
    pointer: {
      elastic: true
    },
    colors: {
      arcColors: ['#2196F3', '#4CAF50', '#F44336']  // Gradient from blue to green to red
    }
  }
};