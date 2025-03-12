import React from "react";
import { GaugeComponent } from "react-gauge-component";
import styled from "styled-components";

const GaugeWrapper = styled.div`
  text-align: center;
  width: 250px; /* Fixed width for uniformity */
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  &:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); }
  h3 { margin: 0 0 10px 0; color: #333; font-size: 1.2rem; }
`;

const ValueBox = styled.div`
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.9rem;
  font-weight: bold;
  color: #333;
  background: #fff;
  padding: 5px 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 2;
`;

const Gauge = ({ title, value, minValue, maxValue, unit }) => {
  const formatValue = (val) => `${val.toFixed(1)}${unit}`;

  return (
    <GaugeWrapper>
      <h3>{title}</h3>
      <div style={{ position: "relative" }}>
        <ValueBox>{formatValue(value)}</ValueBox>
        <GaugeComponent
          value={value}
          minValue={minValue}
          maxValue={maxValue}
          arc={{ width: 0.2, padding: 0.005, cornerRadius: 1 }}
          labels={{ valueLabel: { formatTextValue: () => "" }, tickLabels: { type: "inner", ticks: [{ value: minValue }, { value: (maxValue - minValue) / 2 }, { value: maxValue }] } }}
          pointer={{ elastic: true }}
        />
      </div>
    </GaugeWrapper>
  );
};

export default Gauge;