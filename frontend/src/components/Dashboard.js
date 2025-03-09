import React from "react";

const Dashboard = ({ metrics }) => {
  return (
    <div style={styles.dashboard}>
      <h2 style={styles.heading}>Live Metrics</h2>
      <div style={styles.metricsContainer}>
        {metrics.map((metric, index) => (
          <div key={index} style={styles.metricCard}>
            <h3 style={styles.metricName}>{metric.metric_name}</h3>
            <p style={styles.metricValue}>
              {metric.value} {metric.unit}
            </p>
            <p style={styles.metricDevice}>{metric.device_name}</p>
            <p style={styles.metricTimestamp}>
              {new Date(metric.timestamp).toLocaleString([], {
                year: "numeric",
                month: "numeric",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  dashboard: {
    padding: "20px",
    backgroundColor: "#f5f5f5",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  heading: {
    color: "#3f51b5",
    marginBottom: "20px",
  },
  metricsContainer: {
    display: "flex",
    flexWrap: "wrap",
    gap: "20px",
  },
  metricCard: {
    backgroundColor: "#ffffff",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    flex: "1 1 calc(33.333% - 40px)",
    minWidth: "250px",
  },
  metricName: {
    color: "#333333",
    marginBottom: "10px",
  },
  metricValue: {
    fontSize: "24px",
    fontWeight: "bold",
    color: "#3f51b5",
    marginBottom: "10px",
  },
  metricDevice: {
    color: "#666666",
    marginBottom: "10px",
  },
  metricTimestamp: {
    color: "#999999",
    fontSize: "12px",
  },
};

export default Dashboard;