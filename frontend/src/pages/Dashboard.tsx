import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { portfolioApi, Portfolio, PerformanceMetrics, DiversificationData } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import PerformanceCard from '../components/PerformanceCard';

const Dashboard: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState<number | null>(null);
  const [performance, setPerformance] = useState<PerformanceMetrics | null>(null);
  const [diversification, setDiversification] = useState<DiversificationData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPortfolios();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (selectedPortfolio) {
      loadPortfolioData(selectedPortfolio);
    }
  }, [selectedPortfolio]);

  const loadPortfolios = async () => {
    try {
      const response = await portfolioApi.getAll();
      setPortfolios(response.data);
      if (response.data.length > 0 && !selectedPortfolio) {
        setSelectedPortfolio(response.data[0].id);
      }
    } catch (error) {
      console.error('Error loading portfolios:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPortfolioData = async (portfolioId: number) => {
    try {
      const [perfResponse, divResponse] = await Promise.all([
        portfolioApi.getPerformance(portfolioId),
        portfolioApi.getDiversification(portfolioId),
      ]);
      setPerformance(perfResponse.data);
      setDiversification(divResponse.data);
    } catch (error) {
      console.error('Error loading portfolio data:', error);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

  if (loading) {
    return <LoadingSpinner size="lg" className="h-64" />;
  }

  if (portfolios.length === 0) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900 mb-2">No portfolios found</h3>
        <p className="text-gray-600">Create your first portfolio to get started.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Portfolio Selector */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Select Portfolio</h3>
        <select
          value={selectedPortfolio || ''}
          onChange={(e) => setSelectedPortfolio(Number(e.target.value))}
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          {portfolios.map((portfolio) => (
            <option key={portfolio.id} value={portfolio.id}>
              {portfolio.name}
            </option>
          ))}
        </select>
      </div>

      {performance && (
        <>
          {/* Performance Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <PerformanceCard
              title="Total Value"
              value={formatCurrency(performance.total_value)}
            />
            <PerformanceCard
              title="Total Cost"
              value={formatCurrency(performance.total_cost)}
            />
            <PerformanceCard
              title="Total Gain/Loss"
              value={formatCurrency(performance.total_gain_loss)}
              change={performance.total_gain_loss}
            />
            <PerformanceCard
              title="Return"
              value={`${performance.total_gain_loss_percent.toFixed(2)}%`}
              changePercent={performance.total_gain_loss_percent}
            />
          </div>

          {/* Holdings Performance Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Holdings Performance</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={performance.holdings}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="asset.symbol" />
                  <YAxis />
                  <Tooltip
                    formatter={(value: any, name: string) => [
                      name === 'current_value' || name === 'cost_basis' || name === 'gain_loss'
                        ? formatCurrency(value)
                        : value,
                      name === 'current_value' ? 'Current Value' :
                      name === 'cost_basis' ? 'Cost Basis' :
                      name === 'gain_loss' ? 'Gain/Loss' : name
                    ]}
                  />
                  <Legend />
                  <Bar dataKey="current_value" fill="#3b82f6" name="Current Value" />
                  <Bar dataKey="cost_basis" fill="#6b7280" name="Cost Basis" />
                  <Bar dataKey="gain_loss" fill="#10b981" name="Gain/Loss" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}

      {diversification && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Asset Type Diversification */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Asset Type Allocation</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={Object.entries(diversification.by_asset_type).map(([type, percentage]) => ({
                      name: type.charAt(0).toUpperCase() + type.slice(1),
                      value: percentage,
                    }))}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {Object.entries(diversification.by_asset_type).map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Individual Asset Allocation */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Individual Assets</h3>
            <div className="space-y-3">
              {diversification.by_asset.map((item, index) => (
                <div key={item.asset.id} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div
                      className="w-3 h-3 rounded-full mr-3"
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    />
                    <div>
                      <p className="text-sm font-medium text-gray-900">{item.asset.symbol}</p>
                      <p className="text-xs text-gray-500">{item.asset.name}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      {formatCurrency(item.value)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {item.percentage.toFixed(1)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;