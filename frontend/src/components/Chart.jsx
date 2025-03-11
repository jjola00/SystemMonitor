/* frontend/src/components/Chart.jsx */

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import { Button, MetricHeading } from '../styles/StyledComponents';
import { chartColors } from '../config';
import Loading from './Loading';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

const Chart = ({ metricData, title, loading, metricType }) => {
  if (loading) return <Loading />;
  
  if (!metricData || metricData.length === 0) {
    return <p>No data available for {title}.</p>;
  }

  // Group metrics by name
  const metricsGroupedByName = metricData.reduce((groups, metric) => {
    const name = metric.metrics ? metric.metrics.name : 'Unknown';
    if (!groups[name]) {
      groups[name] = [];
    }
    groups[name].push(metric);
    return groups;
  }, {});

  // Generate datasets for the chart
  const datasets = Object.entries(metricsGroupedByName).map(([metricName, metrics]) => {
    let colorConfig;
    
    // Determine color config based on metric type and name
    if (metricType === 'system') {
      colorConfig = metricName.includes('cpu') ? chartColors.system.cpu : chartColors.system.ram;
    } else if (metricType === 'weather') {
      colorConfig = chartColors.weather.temp;
    } else if (metricType === 'crypto') {
      colorConfig = chartColors.crypto.price;
    }
    
    return {
      label: metricName,
      data: metrics.map(metric => ({
        x: new Date(metric.timestamp),
        y: metric.value
      })),
      borderColor: colorConfig.borderColor,
      backgroundColor: colorConfig.backgroundColor,
    };
  });

  // Sort data points by timestamp
  datasets.forEach(dataset => {
    dataset.data.sort((a, b) => new Date(a.x) - new Date(b.x));
  });

  // Find min and max values for y-axis scaling (with 10% padding)
  const allValues = metricData.map(metric => metric.value);
  const minValue = Math.min(...allValues);
  const maxValue = Math.max(...allValues);
  const yMin = Math.max(0, minValue - (maxValue - minValue) * 0.1);
  const yMax = maxValue + (maxValue - minValue) * 0.1;

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: yMin,
        max: yMax,
      },
      x: {
        type: 'time',
        time: {
          unit: 'minute',
          tooltipFormat: 'PP HH:mm',
          displayFormats: {
            minute: 'HH:mm'
          }
        },
        title: {
          display: true,
          text: 'Time'
        }
      },
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: title,
      },
    },
  };

  // Handle refresh button click
  const handleRefresh = async () => {
    // This would normally fetch fresh data, but our App component already has auto-refresh
    // Here we could trigger an immediate refresh if needed
    window.location.reload();
  };

  return (
    <div style={{ width: '100%', maxWidth: '100%' }}>
      <MetricHeading>{title}</MetricHeading>
      <Button onClick={handleRefresh}>Refresh Data</Button>
      <div style={{ width: '100%', height: '600px' }}>
        <Line options={options} data={{ datasets }} />
      </div>
    </div>
  );
};

export default Chart;