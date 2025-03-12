// Base URL for API calls
export const apiUrl = 'http://localhost:10000/api'; // Matches your FastAPI backend

// Chart color schemes (unchanged)
export const chartColors = {
  system: {
    cpu_usage: { // Updated to match backend metric name
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
    ram_usage: { // Updated to match backend metric name
      borderColor: 'rgb(53, 162, 235)',
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
    }
  },
  weather: {
    weather_temp: { // Updated to match backend metric name
      borderColor: 'rgb(255, 159, 64)',
      backgroundColor: 'rgba(255, 159, 64, 0.5)',
    }
  },
  crypto: {
    crypto_price: { // Updated to match backend metric name
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.5)',
    }
  }
};

// External trading sites for crypto (unchanged)
export const tradingSites = {
  BTC: 'https://www.binance.com/en/trade/BTC_USDT',
};

// Gauge configurations (unchanged)
export const gaugeConfigs = {
  cpu: {
    min: 0,
    max: 100,
    arc: { width: 0.2, padding: 0.05, cornerRadius: 1 },
    pointer: { elastic: true },
    colors: { low: '#4CAF50', medium: '#FFC107', high: '#F44336' }
  },
  ram: {
    min: 0,
    max: 100,
    arc: { width: 0.2, padding: 0.05, cornerRadius: 1 },
    pointer: { elastic: true },
    colors: { low: '#4CAF50', medium: '#FFC107', high: '#F44336' }
  },
  weather: {
    min: -20,
    max: 50,
    arc: { width: 0.2, padding: 0.05, cornerRadius: 1 },
    pointer: { elastic: true },
    colors: { arcColors: ['#2196F3', '#4CAF50', '#F44336'] }
  }
};