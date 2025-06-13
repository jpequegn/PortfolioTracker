import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../../App';

// Mock the API service
jest.mock('../../services/api', () => ({
  portfolioApi: {
    getPortfolios: jest.fn().mockResolvedValue([]),
    getPortfolioPerformance: jest.fn().mockResolvedValue({
      total_value: 0,
      total_cost_basis: 0,
      total_gain_loss: 0,
      total_gain_loss_percentage: 0
    })
  },
  assetApi: {
    getAssets: jest.fn().mockResolvedValue([])
  }
}));

const AppWithRouter = () => (
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<AppWithRouter />);
  });

  test('displays navigation elements', () => {
    render(<AppWithRouter />);
    
    // Check for navigation elements
    expect(screen.getByText(/Portfolio Tracker/i)).toBeInTheDocument();
  });

  test('has proper routing structure', () => {
    render(<AppWithRouter />);
    
    // The app should render without throwing errors
    // More specific routing tests would go here
  });
});