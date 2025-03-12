import React, { useState, useEffect, useCallback } from 'react';
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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    fetchAllMetrics();
  }, []);

  const fetchAllMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [systemResponse, weatherResponse, cryptoResponse] = await Promise.all([
        fetch('/api/metrics/system?limit=10'), // Using proxy
        fetch('/api/metrics/weather?limit=10'),
        fetch('/api/metrics/crypto?limit=10')
      ]);

      if (!systemResponse.ok) throw new Error(`System metrics fetch failed: ${systemResponse.status}`);
      if (!weatherResponse.ok) throw new Error(`Weather metrics fetch failed: ${weatherResponse.status}`);
      if (!cryptoResponse.ok) throw new Error(`Crypto metrics fetch failed: ${cryptoResponse.status}`);

      const systemData = await systemResponse.json();
      const weatherData = await weatherResponse.json();
      const cryptoData = await cryptoResponse.json();

      console.log('System data:', systemData);
      console.log('Weather data:', weatherData);
      console.log('Crypto data:', cryptoData);

      setSystemMetrics(Array.isArray(systemData) ? systemData : []);
      setWeatherMetrics(Array.isArray(weatherData) ? weatherData : []);
      setCryptoMetrics(Array.isArray(cryptoData) ? cryptoData : []);
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const uploadMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const systemPayload = {
        device_name: "test",
        cpu_usage: Math.random() * 100, // Simulate data; replace with real collector data later
        ram_usage: Math.random() * 100,
        timestamp: new Date().toISOString()
      };
      const weatherPayload = { temperature: Math.random() * 30 + 5 }; // Simulate 5-35°C
      const cryptoPayload = { value: Math.random() * 50000 + 20000, unit: "USD" }; // Simulate $20k-$70k

      const [systemUpload, weatherUpload, cryptoUpload] = await Promise.all([
        fetch('/api/metrics/system/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(systemPayload)
        }),
        fetch('/api/metrics/weather/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(weatherPayload)
        }),
        fetch('/api/metrics/crypto/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(cryptoPayload)
        })
      ]);

      if (!systemUpload.ok) throw new Error(`System metrics upload failed: ${systemUpload.status}`);
      if (!weatherUpload.ok) throw new Error(`Weather metrics upload failed: ${weatherUpload.status}`);
      if (!cryptoUpload.ok) throw new Error(`Crypto metrics upload failed: ${cryptoUpload.status}`);

      await fetchAllMetrics();
    } catch (err) {
      console.error('Error uploading metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isUploading) {
      const intervalId = setInterval(uploadMetrics, 10000);
      return () => clearInterval(intervalId);
    }
  }, [isUploading, uploadMetrics]);

  const validSystemMetrics = systemMetrics.filter(metric => metric.metrics !== null);
  const latestCpuUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'cpu_usage')?.value || 0;
  const latestRamUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'ram_usage')?.value || 0;

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Container>
        {loading && <Loading />}
        <HeaderBanner>System Monitoring Dashboard</HeaderBanner>
        <Navigation>
          <NavList>
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/system">System Metrics</Link></li>
            <li><Link to="/weather">Weather Metrics</Link></li>
            <li><Link to="/crypto">Crypto Metrics</Link></li>
          </NavList>
        </Navigation>

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
            <Table 
              systemMetrics={systemMetrics}
              weatherMetrics={weatherMetrics}
              cryptoMetrics={cryptoMetrics}
              loading={loading}
            />
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