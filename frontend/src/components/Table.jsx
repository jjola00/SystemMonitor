import React, { useState } from 'react';
import styled from 'styled-components';

const TableContainer = styled.div`
    width: 100%;
    overflow-x: auto;
    margin-top: 20px;
`;

const StyledTable = styled.table`
    width: 100%;
    border-collapse: collapse;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

const Th = styled.th`
    padding: 12px;
    text-align: left;
    background-color: #f5f5f5;
    border-bottom: 2px solid #ddd;
`;

const Td = styled.td`
    padding: 12px;
    border-bottom: 1px solid #ddd;
`;

const ButtonContainer = styled.div`
    margin-top: 10px;
    display: flex;
    gap: 10px;
`;

const PaginationButton = styled.button`
    padding: 8px 16px;
    background-color: ${props => props.disabled ? '#ccc' : '#007bff'};
    color: white;
    border: none;
    border-radius: 4px;
    cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
    &:hover {
        background-color: ${props => props.disabled ? '#ccc' : '#0056b3'};
    }
`;

const Table = ({ systemMetrics, weatherMetrics, cryptoMetrics, loading }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    const allMetrics = [
        ...(systemMetrics || []).map(m => ({ type: 'System', ...m })),
        ...(weatherMetrics || []).map(m => ({ type: 'Weather', ...m })),
        ...(cryptoMetrics || []).map(m => ({ type: 'Crypto', ...m })),
    ].filter(m => m.metrics !== null);

    const totalItems = allMetrics.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedMetrics = allMetrics.slice(startIndex, startIndex + itemsPerPage);

    const handlePrevious = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    const handleNext = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
    };

    if (loading) return <div>Loading metrics...</div>;
    if (!allMetrics.length) return <div>No metrics available.</div>;

    return (
        <TableContainer>
            <StyledTable>
                <thead>
                    <tr>
                        <Th>Type</Th>
                        <Th>Metric Name</Th>
                        <Th>Value</Th>
                        <Th>Timestamp</Th>
                    </tr>
                </thead>
                <tbody>
                    {paginatedMetrics.map((metric, index) => (
                        <tr key={index}>
                            <Td>{metric.type}</Td>
                            <Td>{metric.metrics?.name || 'N/A'}</Td>
                            <Td>{metric.value}</Td>
                            <Td>{new Date(metric.timestamp).toLocaleString()}</Td>
                        </tr>
                    ))}
                </tbody>
            </StyledTable>
            <ButtonContainer>
                <PaginationButton onClick={handlePrevious} disabled={currentPage === 1}>
                    Previous
                </PaginationButton>
                <span>Page {currentPage} of {totalPages}</span>
                <PaginationButton onClick={handleNext} disabled={currentPage === totalPages}>
                    Next
                </PaginationButton>
            </ButtonContainer>
        </TableContainer>
    );
};

export default Table;