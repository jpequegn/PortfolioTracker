import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import HistoricalData from '../../pages/HistoricalData';
import { assetApi } from '../../services/api';

// Mock the API
jest.mock('../../services/api', () => ({
  assetApi: {
    getHistoricalData: jest.fn(),
  },
}));

// Mock the LoadingSpinner component
jest.mock('../LoadingSpinner', () => {
  return function LoadingSpinner() {
    return <div data-testid="loading-spinner">Loading...</div>;
  };
});

const mockHistoricalData = {
  symbol: 'AAPL',
  name: 'Apple Inc.',
  currency: 'USD',
  exchange: 'NASDAQ',
  period: '1y',
  interval: '1d',
  current_price: 150.0,
  daily_change: 2.5,
  daily_change_percent: 1.69,
  period_change: 25.0,
  period_change_percent: 20.0,
  data: [
    {
      date: '2023-01-01',
      open: 148.0,
      high: 152.0,
      low: 147.0,
      close: 150.0,
      volume: 1000000,
    },
    {
      date: '2023-01-02',
      open: 150.0,
      high: 155.0,
      low: 149.0,
      close: 153.0,
      volume: 1200000,
    },
  ],
  data_points: 2,
};

describe('HistoricalData Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the component with initial state', () => {
    render(<HistoricalData />);
    
    expect(screen.getByText('Historical Market Data')).toBeInTheDocument();
    expect(screen.getByDisplayValue('AAPL')).toBeInTheDocument();
    
    // Check for select elements by their IDs
    const periodSelect = screen.getByLabelText('Period');
    const intervalSelect = screen.getByLabelText('Interval');
    
    expect(periodSelect).toHaveValue('1y');
    expect(intervalSelect).toHaveValue('1d');
    
    // Button shows "Loading..." initially because it auto-fetches data
    expect(screen.getByRole('button', { name: /loading/i })).toBeInTheDocument();
  });

  test('fetches and displays historical data on component mount', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      expect(assetApi.getHistoricalData).toHaveBeenCalledWith('AAPL', '1y', '1d');
    });

    await waitFor(() => {
      expect(screen.getByText('AAPL')).toBeInTheDocument();
      expect(screen.getByText('Apple Inc.')).toBeInTheDocument();
      expect(screen.getAllByText('$150.00')).toHaveLength(3); // Appears in summary and table
    });
  });

  test('handles symbol input change', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: { ...mockHistoricalData, symbol: 'MSFT', name: 'Microsoft Corporation' },
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    const symbolInput = screen.getByDisplayValue('AAPL');
    
    await act(async () => {
      fireEvent.change(symbolInput, { target: { value: 'MSFT' } });
    });

    expect(screen.getByDisplayValue('MSFT')).toBeInTheDocument();

    await waitFor(() => {
      expect(assetApi.getHistoricalData).toHaveBeenCalledWith('MSFT', '1y', '1d');
    });
  });

  test('handles period selection change', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: { ...mockHistoricalData, period: '6mo' },
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    const periodSelect = screen.getByLabelText('Period');
    
    await act(async () => {
      fireEvent.change(periodSelect, { target: { value: '6mo' } });
    });

    expect(periodSelect).toHaveValue('6mo');

    await waitFor(() => {
      expect(assetApi.getHistoricalData).toHaveBeenCalledWith('AAPL', '6mo', '1d');
    });
  });

  test('handles interval selection change', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: { ...mockHistoricalData, interval: '1wk' },
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    const intervalSelect = screen.getByLabelText('Interval');
    
    await act(async () => {
      fireEvent.change(intervalSelect, { target: { value: '1wk' } });
    });

    expect(intervalSelect).toHaveValue('1wk');

    await waitFor(() => {
      expect(assetApi.getHistoricalData).toHaveBeenCalledWith('AAPL', '1y', '1wk');
    });
  });

  test('displays loading state', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ data: mockHistoricalData }), 100))
    );

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    });
  });

  test('displays error message when API call fails', async () => {
    const errorMessage = 'Failed to fetch historical data';
    (assetApi.getHistoricalData as jest.Mock).mockRejectedValue({
      response: { data: { detail: errorMessage } },
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      expect(screen.getByText('Error')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('displays historical data table', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      expect(screen.getByText('Historical Prices')).toBeInTheDocument();
      expect(screen.getByText('Date')).toBeInTheDocument();
      expect(screen.getByText('Open')).toBeInTheDocument();
      expect(screen.getByText('High')).toBeInTheDocument();
      expect(screen.getByText('Low')).toBeInTheDocument();
      expect(screen.getByText('Close')).toBeInTheDocument();
      expect(screen.getByText('Volume')).toBeInTheDocument();
    });

    // Check if data rows are displayed
    await waitFor(() => {
      expect(screen.getByText('1/1/2023')).toBeInTheDocument();
      expect(screen.getByText('1/2/2023')).toBeInTheDocument();
      expect(screen.getByText('1,000,000')).toBeInTheDocument();
      expect(screen.getByText('1,200,000')).toBeInTheDocument();
    });
  });

  test('displays stock information correctly', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      expect(screen.getByText('AAPL')).toBeInTheDocument();
      expect(screen.getByText('Apple Inc.')).toBeInTheDocument();
      expect(screen.getByText('NASDAQ')).toBeInTheDocument();
      expect(screen.getAllByText('$150.00')).toHaveLength(3); // Appears in summary and table
      expect(screen.getByText('+20.00%')).toBeInTheDocument(); // period change
      expect(screen.getByText('2')).toBeInTheDocument(); // data points
    });
  });

  test('handles form submission', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    const form = screen.getByRole('button', { name: /get data/i }).closest('form');
    
    await act(async () => {
      fireEvent.submit(form!);
    });

    await waitFor(() => {
      expect(assetApi.getHistoricalData).toHaveBeenCalledWith('AAPL', '1y', '1d');
    });
  });

  test('formats currency correctly', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      // Check if currency is formatted correctly
      expect(screen.getAllByText('$150.00')).toHaveLength(3); // Appears in summary and table
      expect(screen.getByText('$148.00')).toBeInTheDocument();
      expect(screen.getByText('$152.00')).toBeInTheDocument();
    });
  });

  test('formats percentage correctly', async () => {
    (assetApi.getHistoricalData as jest.Mock).mockResolvedValue({
      data: mockHistoricalData,
    });

    await act(async () => {
      render(<HistoricalData />);
    });

    await waitFor(() => {
      // Check if percentages are formatted correctly
      expect(screen.getByText('+20.00%')).toBeInTheDocument(); // period change
    });
  });
});