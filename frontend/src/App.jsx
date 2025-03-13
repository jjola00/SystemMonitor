import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, HeaderBanner, Navigation, NavList, Link, ErrorContainer, RetryButton, Button } from './styles/StyledComponents';
import Chart from './components/Chart';
import Gauge from './components/Gauge';
import MetricBox from './components/IconMetric';
import Table from './components/Table';
import Loading from './components/Loading';
import { FaTemperatureHigh, FaBitcoin } from 'react-icons/fa';
import { apiUrl } from './config';  // Import apiUrl

function App() {
  const [systemMetrics, setSystemMetrics] = useState([]);
  const [weatherMetrics, setWeatherMetrics] = useState([]);
  const [cryptoMetrics, setCryptoMetrics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAllMetrics();
  }, []);

  const fetchAllMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [systemResponse, weatherResponse, cryptoResponse] = await Promise.all([
        fetch(`${apiUrl}/metrics/system?limit=30`),
        fetch(`${apiUrl}/metrics/weather?limit=30`),
        fetch(`${apiUrl}/metrics/crypto?limit=30`)
      ]);

      if (!systemResponse.ok) throw new Error(`System metrics fetch failed: ${systemResponse.status}`);
      if (!weatherResponse.ok) throw new Error(`Weather metrics fetch failed: ${weatherResponse.status}`);
      if (!cryptoResponse.ok) throw new Error(`Crypto metrics fetch failed: ${cryptoResponse.status}`);

      const systemData = await systemResponse.json();
      const weatherData = await weatherResponse.json();
      const cryptoData = await cryptoResponse.json();

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

  const sendCommand = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiUrl}/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_name: 'test', command: 'open_task_manager' })
      });
      if (!response.ok) throw new Error(`Command failed: ${response.status}`);
      console.log('Command sent successfully');
    } catch (err) {
      console.error('Error sending command:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const validSystemMetrics = systemMetrics.filter(metric => metric.metrics !== null);
  const latestCpuUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'cpu_usage')?.value || 0;
  const latestRamUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'ram_usage')?.value || 0;
  const latestTemp = weatherMetrics.find(metric => metric.metrics?.name === 'weather_temp')?.value || 0;
  const latestCrypto = cryptoMetrics.find(metric => metric.metrics?.name === 'crypto_price')?.value || 0;

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

        <Button onClick={sendCommand} style={{ marginBottom: '20px' }}>
          Open Task Manager
        </Button>

        {error && (
          <ErrorContainer>
            <p>Error: {error}</p>
            <RetryButton onClick={fetchAllMetrics}>Retry Fetch</RetryButton>
          </ErrorContainer>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '20px', marginBottom: '20px', flexWrap: 'wrap' }}>
          <Gauge title="CPU Usage" value={latestCpuUsage} minValue={0} maxValue={100} unit="%" />
          <Gauge title="RAM Usage" value={latestRamUsage} minValue={0} maxValue={100} unit="%" />
          <MetricBox title="Temperature" value={latestTemp} unit="°C" icon={<FaTemperatureHigh />} />
          <MetricBox title="Bitcoin Price" value={latestCrypto} unit="$" icon={<FaBitcoin />} />
        </div>
        
        <Routes>
          <Route path="/" element={<Table systemMetrics={systemMetrics} weatherMetrics={weatherMetrics} cryptoMetrics={cryptoMetrics} loading={loading} />} />
          <Route path="/system" element={<Chart metricData={systemMetrics} title="System Metrics" loading={loading} metricType="system" />} />
          <Route path="/weather" element={<Chart metricData={weatherMetrics} title="Weather Metrics" loading={loading} metricType="weather" />} />
          <Route path="/crypto" element={<Chart metricData={cryptoMetrics} title="Crypto Metrics" loading={loading} metricType="crypto" />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;