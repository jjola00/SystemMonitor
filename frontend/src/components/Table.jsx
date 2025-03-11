import React from 'react';
import styled from 'styled-components';
import { MetricHeading } from '../styles/StyledComponents';
import Loading from './Loading';

const StyledTable = styled.table`
  border-collapse: collapse;
  margin: 25px 0;
  font-size: 0.9em;
  font-family: sans-serif;
  min-width: 400px;
  width: 100%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
`;

const TableHead = styled.thead`
  background-color: #009879;
  color: #ffffff;
  text-align: left;
  position: sticky;
  top: 0;
`;

const TableBody = styled.tbody`
  tr {
    border-bottom: 1px solid #dddddd;
    
    &:nth-of-type(even) {
      background-color: #f3f3f3;
    }
    
    &:last-of-type {
      border-bottom: 2px solid #009879;
    }
  }
`;

const TableRow = styled.tr``;

const TableHeader = styled.th`
  padding: 12px 15px;
`;

const TableCell = styled.td`
  padding: 12px 15px;
`;

const TabContainer = styled.div`
  margin-top: 20px;
`;

const TabButtons = styled.div`
  display: flex;
  margin-bottom: 10px;
`;

const TabButton = styled.button`
  padding: 10px 20px;
  background-color: ${props => props.active ? '#009879' : '#f1f1f1'};
  color: ${props => props.active ? 'white' : 'black'};
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:hover {
    background-color: ${props => props.active ? '#007965' : '#ddd'};
  }
`;

const PaginationContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 10px;
`;

const PaginationButton = styled.button`
  background-color: #009879;
  color: white;
  border: none;
  padding: 10px;
  margin: 0 5px;
  cursor: pointer;
  border-radius: 5px;

  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

const Table = ({ systemMetrics, weatherMetrics, cryptoMetrics, loading }) => {
  const [activeTab, setActiveTab] = React.useState('system');
  const [currentPage, setCurrentPage] = React.useState(0);
  const itemsPerPage = 10;

  if (loading) return <Loading />;

  const getPaginatedData = (data) => {
    const startIndex = currentPage * itemsPerPage;
    return data.slice(startIndex, startIndex + itemsPerPage);
  };

  const renderTable = () => {
    let data;
    let columns;
    
    switch(activeTab) {
      case 'system':
        data = systemMetrics;
        columns = ['Metric', 'Value', 'Timestamp'];
        break;
      case 'weather':
        data = weatherMetrics;
        columns = ['Metric', 'Value (°C)', 'Timestamp'];
        break;
      case 'crypto':
        data = cryptoMetrics;
        columns = ['Metric', 'Value (USD)', 'Timestamp'];
        break;
      default:
        data = [];
        columns = [];
    }
    
    if (!data || data.length === 0) {
      return <p>No data available for {activeTab} metrics.</p>;
    }

    const paginatedData = getPaginatedData(data);
    const totalPages = Math.ceil(data.length / itemsPerPage);

    return (
      <>
        <StyledTable>
          <TableHead>
            <TableRow>
              {columns.map((column, index) => (
                <TableHeader key={index}>{column}</TableHeader>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.metrics ? row.metrics.name : 'Unknown'}</TableCell>
                <TableCell>{row.value.toFixed(2)}</TableCell>
                <TableCell>{formatDate(row.timestamp)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </StyledTable>
        <PaginationContainer>
          <PaginationButton onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 0}>
            Previous
          </PaginationButton>
          <span>Page {currentPage + 1} of {totalPages}</span>
          <PaginationButton onClick={() => setCurrentPage(currentPage + 1)} disabled={currentPage >= totalPages - 1}>
            Next
          </PaginationButton>
        </PaginationContainer>
      </>
    );
  };
  
  return (
    <>
      <MetricHeading>Metrics History</MetricHeading>
      <TabContainer>
        <TabButtons>
          <TabButton 
            active={activeTab === 'system'} 
            onClick={() => setActiveTab('system')}
          >
            System Metrics
          </TabButton>
          <TabButton 
            active={activeTab === 'weather'} 
            onClick={() => setActiveTab('weather')}
          >
            Weather Metrics
          </TabButton>
          <TabButton 
            active={activeTab === 'crypto'} 
            onClick={() => setActiveTab('crypto')}
          >
            Crypto Metrics
          </TabButton>
        </TabButtons>
        {renderTable()}
      </TabContainer>
    </>
  );
};

export default Table;