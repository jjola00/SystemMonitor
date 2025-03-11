import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { 
  Container, 
  HeaderBanner, 
  Navigation, 
  NavList, 
  Link, 
  ErrorContainer,
  RetryButton
} from './styles/StyledComponents';  // Fixed import path
import Chart from './components/Chart';  // Fixed import path
import Gauge from './components/Gauge';  // Fixed import path
import Table from './components/Table';  // Fixed import path

function App() {
  const [systemMetrics, setSystemMetrics] = useState([]);
  const [weatherMetrics, setWeatherMetrics] = useState([]);
  const [cryptoMetrics, setCryptoMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAllMetrics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch system metrics
      const systemResponse = await fetch('/api/metrics/system');
      if (!systemResponse.ok) throw new Error('Failed to fetch system metrics');
      const systemData = await systemResponse.json();
      setSystemMetrics(systemData);
      
      // Fetch weather metrics
      const weatherResponse = await fetch('/api/metrics/weather');
      if (!weatherResponse.ok) throw new Error('Failed to fetch weather metrics');
      const weatherData = await weatherResponse.json();
      setWeatherMetrics(weatherData);
      
      // Fetch crypto metrics
      const cryptoResponse = await fetch('/api/metrics/crypto');
      if (!cryptoResponse.ok) throw new Error('Failed to fetch crypto metrics');
      const cryptoData = await cryptoResponse.json();
      setCryptoMetrics(cryptoData);

    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllMetrics();
    
    // Set up interval to refresh data every 30 seconds
    const intervalId = setInterval(fetchAllMetrics, 30000);
    
    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <Router>
      <Container>
        <HeaderBanner>System Monitoring Dashboard</HeaderBanner>
        <Navigation>
          <NavList>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/system">System Metrics</Link></li>
            <li><Link to="/weather">Weather Metrics</Link></li>
            <li><Link to="/crypto">Crypto Metrics</Link></li>
          </NavList>
        </Navigation>

        {error && (
          <ErrorContainer>
            <p>Error: {error}</p>
            <RetryButton onClick={fetchAllMetrics}>Retry</RetryButton>
          </ErrorContainer>
        )}
        
        <Routes>
          <Route path="/" element={
            <>
              <Gauge 
                systemMetrics={systemMetrics} 
                weatherMetrics={weatherMetrics} 
                loading={loading} 
              />
              <Table 
                systemMetrics={systemMetrics}
                weatherMetrics={weatherMetrics}
                cryptoMetrics={cryptoMetrics}
                loading={loading}
              />
            </>
          } />
          <Route path="/system" element={
            <Chart 
              metricData={systemMetrics} 
              title="System Metrics" 
              loading={loading}
              metricType="system"
            />
          } />
          <Route path="/weather" element={
            <Chart 
              metricData={weatherMetrics} 
              title="Weather Metrics" 
              loading={loading}
              metricType="weather"
            />
          } />
          <Route path="/crypto" element={
            <Chart 
              metricData={cryptoMetrics} 
              title="Crypto Metrics" 
              loading={loading}
              metricType="crypto"
            />
          } />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;