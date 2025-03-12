import React from "react";
import styled from "styled-components";

const MetricBoxWrapper = styled.div`
  text-align: center;
  width: 250px; /* Matches Gauge width */
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  &:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); }
  h3 { margin: 0 0 10px 0; color: #333; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; gap: 5px; }
`;

const ValueDisplay = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-top: 20px;
`;

const MetricBox = ({ title, value, unit, icon }) => {
  const formatValue = (val) => unit === "$" ? `${unit}${val.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : `${val.toFixed(1)}${unit}`;

  return (
    <MetricBoxWrapper>
      <h3>{icon} {title}</h3>
      <ValueDisplay>{formatValue(value)}</ValueDisplay>
    </MetricBoxWrapper>
  );
};

export default MetricBox;