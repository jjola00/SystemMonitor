import React from 'react';
import GaugeComponent from 'react-gauge-component';
import { GaugeContainer, GridContainer, Card, MetricHeading } from '../styles/StyledComponents';
import { gaugeConfigs } from '../config';
import Loading from './Loading';

const Gauge = ({ systemMetrics, weatherMetrics, loading }) => {
  // Get latest metrics
  const getLatestMetricValue = (metrics, metricName) => {
    if (!metrics || metrics.length === 0) return 0;
    
    const filteredMetrics = metrics.filter(metric => 
      metric.metrics && metric.metrics.name === metricName
    );
    
    if (filteredMetrics.length === 0) return 0;
    
    // Sort by timestamp in descending order and get the first (latest) value
    return filteredMetrics
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0].value;
  };

  const cpuUsage = getLatestMetricValue(systemMetrics, 'cpu_usage');
  const ramUsage = getLatestMetricValue(systemMetrics, 'ram_usage');
  const temperature = getLatestMetricValue(weatherMetrics, 'weather_temp');

  if (loading) return <Loading />;

  return (
    <>
      <MetricHeading>Current System Status</MetricHeading>
      <GridContainer>
        <Card>
          <GaugeContainer>
            <h2>CPU Usage</h2>
            <GaugeComponent
              id="cpu-gauge"
              value={cpuUsage}
              type="radial"
              labels={{
                valueLabel: {
                  formatTextValue: value => value + '%',
                  style: { fontSize: '45px', fill: '#000' }
                }
              }}
              arc={gaugeConfigs.cpu.arc}
              pointer={gaugeConfigs.cpu.pointer}
              colors={{
                arcColors: [
                  gaugeConfigs.cpu.colors.low,
                  gaugeConfigs.cpu.colors.medium,
                  gaugeConfigs.cpu.colors.high
                ],
                arcDelimiters: [30, 70]
              }}
              maxValue={100}
              minValue={0}
            />
          </GaugeContainer>
        </Card>
        
        <Card>
          <GaugeContainer>
            <h2>RAM Usage</h2>
            <GaugeComponent
              id="ram-gauge"
              value={ramUsage}
              type="radial"
              labels={{
                valueLabel: {
                  formatTextValue: value => value + '%',
                  style: { fontSize: '45px', fill: '#000' }
                }
              }}
              arc={gaugeConfigs.ram.arc}
              pointer={gaugeConfigs.ram.pointer}
              colors={{
                arcColors: [
                  gaugeConfigs.ram.colors.low,
                  gaugeConfigs.ram.colors.medium, 
                  gaugeConfigs.ram.colors.high
                ],
                arcDelimiters: [30, 70]
              }}
              maxValue={100}
              minValue={0}
            />
          </GaugeContainer>
        </Card>
        
        <Card>
          <GaugeContainer>
            <h2>Current Temperature</h2>
            <GaugeComponent
              id="temp-gauge"
              value={temperature}
              type="radial"
              labels={{
                valueLabel: {
                  formatTextValue: value => value + '°C',
                  style: { fontSize: '45px', fill: '#000' }
                }
              }}
              arc={gaugeConfigs.weather.arc}
              pointer={gaugeConfigs.weather.pointer}
              colors={{
                arcColors: [
                  gaugeConfigs.weather.colors.low,
                  gaugeConfigs.weather.colors.medium,
                  gaugeConfigs.weather.colors.high
                ],
                // Fixed: Set arc delimiters within the min-max range of the weather gauge (-10 to 40)
                arcDelimiters: [5, 25]
              }}
              // Explicitly set min/max values from config to ensure consistency
              maxValue={gaugeConfigs.weather.max}
              minValue={gaugeConfigs.weather.min}
            />
          </GaugeContainer>
        </Card>
      </GridContainer>
    </>
  );
};

export default Gauge;