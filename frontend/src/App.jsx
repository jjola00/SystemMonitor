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
} from './styles/StyledComponents';
import Chart from './components/Chart';
import Gauge from './components/Gauge';
import Table from './components/Table';
import Loading from './components/Loading';

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
      const [systemResponse, weatherResponse, cryptoResponse] = await Promise.all([
        fetch('/api/metrics/system'),
        fetch('/api/metrics/weather'),
        fetch('/api/metrics/crypto')
      ]);

      if (!systemResponse.ok || !weatherResponse.ok || !cryptoResponse.ok) {
        throw new Error('Failed to fetch metrics');
      }

      const [systemData, weatherData, cryptoData] = await Promise.all([
        systemResponse.json(),
        weatherResponse.json(),
        cryptoResponse.json()
      ]);

      setSystemMetrics(systemData);
      setWeatherMetrics(weatherData);
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
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
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