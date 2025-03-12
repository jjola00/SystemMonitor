import React from 'react';
import styled from 'styled-components';

const MetricContainer = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const Title = styled.h3`
  margin-top: 0;
  margin-bottom: 10px;
`;

const Value = styled.div`
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-top: 15px;
`;

const IconContainer = styled.div`
  font-size: 64px;
  color: ${props => props.color || '#4CAF50'};
  margin: 10px 0;
`;

const IconMetric = ({ title, value, icon, unit = '', color }) => {
  return (
    <MetricContainer>
      <Title>{title}</Title>
      <IconContainer color={color}>
        {icon}
      </IconContainer>
      <Value>{value}{unit}</Value>
    </MetricContainer>
  );
};

export default IconMetric;