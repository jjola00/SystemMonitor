import React from 'react';
import { GaugeComponent } from 'react-gauge-component';
import styled from 'styled-components';

const GaugeWrapper = styled.div`
  text-align: center;
  width: 300px;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  h3 {
    margin: 0 0 10px 0;
    color: #333;
    font-size: 1.2rem;
  }
`;

const Gauge = ({ title, value, minValue, maxValue, unit }) => {
  return (
    <GaugeWrapper>
      <h3>{title}</h3>
      <GaugeComponent
        value={value}
        minValue={minValue}
        maxValue={maxValue}
        arc={{
          width: 0.2,
          padding: 0.005,
          cornerRadius: 1,
          colorArray: ['#5BE12C', '#EA4228'], // Gradient from green to red
        }}
        labels={{
          valueLabel: { formatTextValue: value => `${value}${unit}` },
          tickLabels: {
            type: 'inner',
            ticks: [
              { value: minValue },
              { value: (maxValue - minValue) / 2 },
              { value: maxValue },
            ],
          },
        }}
        pointer={{
          elastic: true,
        }}
      />
    </GaugeWrapper>
  );
};

export default Gauge;