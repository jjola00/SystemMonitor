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
  const [loading, setLoading] = useState(false); // For upload process
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false); // State to track if uploading is active

  // Fetch metrics history on initial load
  useEffect(() => {
    fetchAllMetrics();
  }, []);

  const fetchAllMetrics = async () => {
    try {
      // First, get all responses
      const systemResponse = await fetch('https://my-fastapi-backend-miau.onrender.com/api/metrics/system');
      const weatherResponse = await fetch('https://my-fastapi-backend-miau.onrender.com/api/metrics/weather');
      const cryptoResponse = await fetch('https://my-fastapi-backend-miau.onrender.com/api/metrics/crypto');
  
      // Check if responses are OK
      if (!systemResponse.ok) {
        throw new Error(`System metrics fetch failed: ${systemResponse.status}`);
      }
      if (!weatherResponse.ok) {
        throw new Error(`Weather metrics fetch failed: ${weatherResponse.status}`);
      }
      if (!cryptoResponse.ok) {
        throw new Error(`Crypto metrics fetch failed: ${cryptoResponse.status}`);
      }
  
      // Then parse the JSON from each response
      const systemData = await systemResponse.json();
      const weatherData = await weatherResponse.json();
      const cryptoData = await cryptoResponse.json();
  
      console.log('System data:', systemData);
      console.log('Weather data:', weatherData);
      console.log('Crypto data:', cryptoData);
  
      // Set the state variables
      setSystemMetrics(systemData);
      setWeatherMetrics(weatherData);
      setCryptoMetrics(cryptoData);
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError(err.message);
    }
  };

  const uploadMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);
  
    try {
      // Make the upload requests one by one
      const systemUpload = await fetch('https://my-fastapi-backend-miau.onrender.com//api/metrics/system/upload', { method: 'POST' });
      const weatherUpload = await fetch('https://my-fastapi-backend-miau.onrender.com//api/metrics/weather/upload', { method: 'POST' });
      const cryptoUpload = await fetch('https://my-fastapi-backend-miau.onrender.com/api/metrics/crypto/upload', { method: 'POST' });
  
      // Check if they were successful
      if (!systemUpload.ok) {
        throw new Error(`System metrics upload failed: ${systemUpload.status}`);
      }
      if (!weatherUpload.ok) {
        throw new Error(`Weather metrics upload failed: ${weatherUpload.status}`);
      }
      if (!cryptoUpload.ok) {
        throw new Error(`Crypto metrics upload failed: ${cryptoUpload.status}`);
      }
  
      // After uploading, fetch the updated metrics
      await fetchAllMetrics();
    } catch (err) {
      console.error('Error uploading metrics:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []); // Add dependencies if needed

  // Start uploading metrics when isUploading is true
  useEffect(() => {
    if (isUploading) {
      const intervalId = setInterval(uploadMetrics, 10000); // Upload every 10 seconds
      return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }
  }, [isUploading, uploadMetrics]); // Include uploadMetrics in the dependency array

  const validSystemMetrics = systemMetrics.filter(metric => metric.metrics !== null);

  // Get the latest CPU and RAM usage values
  const latestCpuUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'cpu_usage')?.value || 0;
  const latestRamUsage = validSystemMetrics.find(metric => metric.metrics?.name === 'ram_usage')?.value || 0;

  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Container>
        {/* Render the Loading component if loading is true */}
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