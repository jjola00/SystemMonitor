import React from "react";

const MetricsTable = ({ metrics }) => {
  return (
    <div style={styles.tableContainer}>
      <h2 style={styles.heading}>Metrics History</h2>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Device</th>
            <th style={styles.th}>Metric</th>
            <th style={styles.th}>Value</th>
            <th style={styles.th}>Unit</th>
            <th style={styles.th}>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((metric, index) => (
            <tr key={index} style={styles.tr}>
              <td style={styles.td}>{metric.device_name}</td>
              <td style={styles.td}>{metric.metric_name}</td>
              <td style={styles.td}>{metric.value}</td>
              <td style={styles.td}>{metric.unit}</td>
              <td style={styles.td}>
                {new Date(metric.timestamp).toLocaleString([], {
                  year: 'numeric',
                  month: 'numeric',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  tableContainer: {
    padding: "20px",
    backgroundColor: "#f5f5f5",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    marginTop: "20px",
  },
  heading: {
    color: "#3f51b5",
    marginBottom: "20px",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
  th: {
    backgroundColor: "#3f51b5",
    color: "#ffffff",
    padding: "12px",
    textAlign: "left",
  },
  tr: {
    backgroundColor: "#ffffff",
  },
  td: {
    padding: "12px",
    borderBottom: "1px solid #dddddd",
  },
};

export default MetricsTable;