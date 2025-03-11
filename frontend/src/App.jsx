import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { 
  Container, 
  HeaderBanner, 
  Navigation, 
  NavList, 
  Link, 
  ErrorContainer,
  RetryButton,
  Button
} from './styles/StyledComponents';
import Chart from './components/Chart';
import Gauge from './components/Gauge';
import Table from './components/Table';
import Loading from './components/Loading';

function App() {
  const [systemMetrics, setSystemMetrics] = useState([]);
  const [weatherMetrics, setWeatherMetrics] = useState([]);
  const [cryptoMetrics, setCryptoMetrics] = useState([]);
  const [loading, setLoading] = useState(false); // For upload process
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false); // State to track if uploading is active

  // Fetch metrics history on initial load
  useEffect(() => {
    fetchAllMetrics();
  }, []);

  // Fetch all metrics (history)
  const fetchAllMetrics = async () => {
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
    }
  };

  // Upload metrics
  const uploadMetrics = async () => {
    setLoading(true);
    setError(null);

    try {
      const [systemUpload, weatherUpload, cryptoUpload] = await Promise.all([
        fetch('/api/metrics/system/upload', { method: 'POST' }),
        fetch('/api/metrics/weather/upload', { method: 'POST' }),
        fetch('/api/metrics/crypto/upload', { method: 'POST' })
      ]);

      if (!systemUpload.ok || !weatherUpload.ok || !cryptoUpload.ok) {
        throw new Error('Failed to upload metrics');
      }

      // After uploading, fetch the updated metrics
      await fetchAllMetrics();
    } catch (err) {
      console.error('Error uploading metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Start uploading metrics when isUploading is true
  useEffect(() => {
    if (isUploading) {
      const intervalId = setInterval(uploadMetrics, 30000); // Upload every 30 seconds
      return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }
  }, [isUploading]);

  // Get the latest CPU and RAM usage values
  const latestCpuUsage = systemMetrics.find(metric => metric.metrics?.name === 'cpu_usage')?.value || 0;
  const latestRamUsage = systemMetrics.find(metric => metric.metrics?.name === 'ram_usage')?.value || 0;

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

        {/* Button to start/stop uploading metrics */}
        <Button 
          onClick={() => setIsUploading(!isUploading)} 
          style={{ marginBottom: '20px' }}
        >
          {isUploading ? 'Stop Uploading Metrics' : 'Start Uploading Metrics'}
        </Button>

        {error && (
          <ErrorContainer>
            <p>Error: {error}</p>
            <RetryButton onClick={uploadMetrics}>Retry</RetryButton>
          </ErrorContainer>
        )}

        {/* Gauges for CPU and RAM Usage */}
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          <Gauge 
            title="CPU Usage" 
            value={latestCpuUsage} 
            minValue={0} 
            maxValue={100} 
            unit="%"
          />
          <Gauge 
            title="RAM Usage" 
            value={latestRamUsage} 
            minValue={0} 
            maxValue={100} 
            unit="%"
          />
        </div>
        
        <Routes>
          <Route path="/" element={
            <>
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