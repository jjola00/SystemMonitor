// frontend/src/styles/StyledComponents.jsx
import styled from 'styled-components';
import { Link as RouterLink } from 'react-router-dom';

// Layout components
export const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

export const HeaderBanner = styled.h1`
  background-color: #009879;
  color: white;
  padding: 20px;
  text-align: center;
  margin-top: 0;
  border-radius: 5px 5px 0 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

export const Navigation = styled.nav`
  background-color: #f1f1f1;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 0 0 5px 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

export const NavList = styled.ul`
  list-style-type: none;
  display: flex;
  padding: 0;
  margin: 0;
  
  li {
    margin-right: 20px;
    
    &:last-child {
      margin-right: 0;
    }
  }
`;

export const Link = styled(RouterLink)`
  text-decoration: none;
  color: #009879;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 3px;
  transition: background-color 0.3s, color 0.3s;
  
  &:hover {
    background-color: #009879;
    color: white;
  }
  
  &.active {
    background-color: #009879;
    color: white;
  }
`;

// Card and grid components
export const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

export const Card = styled.div`
  background-color: white;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
`;

// Button components
export const Button = styled.button`
  background-color: #009879;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin: 10px 0;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: #007965;
  }
`;

export const RetryButton = styled(Button)`
  background-color: #f44336;
  
  &:hover {
    background-color: #d32f2f;
  }
`;

// Container components
export const GaugeContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 270px;
  
  h2 {
    margin-top: 0;
    color: #333;
  }
`;

export const ErrorContainer = styled.div`
  background-color: #ffebee;
  border-left: 4px solid #f44336;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 4px;
  
  p {
    color: #d32f2f;
    margin: 0 0 10px 0;
  }
`;

// Typography components
export const MetricHeading = styled.h2`
  color: #333;
  border-bottom: 2px solid #009879;
  padding-bottom: 10px;
  margin-top: 30px;
`;