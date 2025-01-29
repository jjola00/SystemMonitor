import { useEffect, useState } from "react";

function App() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/metrics") // Adjust this URL if needed
      .then((res) => res.json())
      .then((data) => setMetrics(data))
      .catch((err) => console.error("Error fetching metrics:", err));
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-6">System Monitor Dashboard</h1>
      <div className="w-full max-w-4xl bg-gray-800 p-6 rounded-lg shadow-lg">
        {metrics.length > 0 ? (
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-700">
                <th className="p-2">Timestamp</th>
                <th className="p-2">CPU Usage (%)</th>
                <th className="p-2">RAM Usage (%)</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((metric, index) => (
                <tr key={index} className="border-b border-gray-700">
                  <td className="p-2">{metric.timestamp}</td>
                  <td className="p-2">{metric.cpu_usage}</td>
                  <td className="p-2">{metric.ram_usage}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Loading metrics...</p>
        )}
      </div>
    </div>
  );
}

export default App;
