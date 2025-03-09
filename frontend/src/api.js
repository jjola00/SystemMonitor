const API_BASE_URL = process.env.REACT_APP_API_URL;

export const fetchMetrics = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch metrics:", error);
    return [];
  }
};

export const startCollector = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/start-collector`, {
      method: "POST",
    });
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed to start collector:", error);
    throw error;
  }
};

export const stopCollector = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stop-collector`, {
      method: "POST",
    });
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed to stop collector:", error);
    throw error;
  }
};