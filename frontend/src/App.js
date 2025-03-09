import React, { useState, useEffect } from "react";
import { fetchMetrics, startCollector, stopCollector } from "./api";
import Dashboard from "./components/Dashboard";
import MetricsTable from "./components/MetricsTable";
import Navbar from "./components/Navbar";

const App = () => {
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [liveMetrics, setLiveMetrics] = useState([]); 
  const [isCollectorRunning, setIsCollectorRunning] = useState(false); 

  useEffect(() => {
    const loadMetricsHistory = async () => {
      const data = await fetchMetrics();
      setMetricsHistory(data);
    };
    loadMetricsHistory();
  }, []);

  const handleToggleCollector = async () => {
    try {
      if (isCollectorRunning) {
        await stopCollector(); 
        setLiveMetrics([]); 
      } else {
        await startCollector();
      }
      setIsCollectorRunning((prev) => !prev);
    } catch (error) {
      console.error("Failed to toggle collector:", error);
    }
  };

  useEffect(() => {
    let interval;
    if (isCollectorRunning) {
      interval = setInterval(async () => {
        const data = await fetchMetrics();
        setLiveMetrics((prevMetrics) => {
          const newMetrics = [data[0], ...prevMetrics]; 
          return newMetrics.slice(0, 6); 
        });
      }, 5000);
    }

    return () => clearInterval(interval); 
  }, [isCollectorRunning]);
                                                                                                      0
  return (
    <div style={styles.app}>
      <Navbar />
      <div style={styles.content}>
        <MetricsTable metrics={metricsHistory} />
        <button onClick={handleToggleCollector} style={styles.button}>
          {isCollectorRunning ? "Stop Viewing" : "View Live Metrics"}
        </button>
        {isCollectorRunning && <Dashboard metrics={liveMetrics} />}
      </div>
    </div>
  );
};

const styles = {
  app: {
    fontFamily: "Arial, sans-serif",
  },
  content: {
    padding: "20px",
  },
  button: {
    backgroundColor: "#3f51b5",
    color: "#ffffff",
    padding: "10px 20px",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    marginBottom: "20px",
  },
};

export default App;