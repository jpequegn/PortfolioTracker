import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:12000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Portfolio {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface Asset {
  id: number;
  symbol: string;
  name: string;
  asset_type: 'stock' | 'bond' | 'etf' | 'cash';
  exchange?: string;
  currency?: string;
  current_price?: string;
  last_updated?: string;
  created_at: string;
}

export interface Holding {
  id: number;
  portfolio_id: number;
  asset_id: number;
  quantity: string;
  average_cost: string;
  created_at: string;
  updated_at?: string;
  asset: Asset;
}

export interface Transaction {
  id: number;
  portfolio_id: number;
  asset_id: number;
  transaction_type: 'buy' | 'sell' | 'dividend' | 'split' | 'deposit' | 'withdrawal';
  quantity: string;
  price: string;
  fees: string;
  total_amount: string;
  transaction_date: string;
  notes?: string;
  created_at: string;
  asset?: Asset;
}

export interface PerformanceMetrics {
  portfolio_id: number;
  total_value: number;
  total_cost: number;
  total_gain_loss: number;
  total_gain_loss_percent: number;
  holdings: {
    asset: Asset;
    quantity: number;
    average_cost: number;
    current_price: number;
    current_value: number;
    cost_basis: number;
    gain_loss: number;
    gain_loss_percent: number;
  }[];
}

export interface DiversificationData {
  total_value: number;
  by_asset_type: Record<string, number>;
  by_asset: {
    asset: Asset;
    value: number;
    percentage: number;
  }[];
}

// API Functions
export const portfolioApi = {
  getAll: () => api.get<Portfolio[]>('/portfolios/'),
  getById: (id: number) => api.get<Portfolio>(`/portfolios/${id}`),
  create: (data: Omit<Portfolio, 'id' | 'created_at' | 'updated_at'>) => 
    api.post<Portfolio>('/portfolios/', data),
  update: (id: number, data: Partial<Portfolio>) => 
    api.put<Portfolio>(`/portfolios/${id}`, data),
  delete: (id: number) => api.delete(`/portfolios/${id}`),
  getPerformance: (id: number) => api.get<PerformanceMetrics>(`/portfolios/${id}/performance`),
  getDiversification: (id: number) => api.get<DiversificationData>(`/portfolios/${id}/diversification`),
};

export const assetApi = {
  getAll: () => api.get<Asset[]>('/assets/'),
  getById: (id: number) => api.get<Asset>(`/assets/${id}`),
  lookup: (symbol: string) => api.get<Asset>(`/assets/lookup/${symbol}`),
  create: (data: Omit<Asset, 'id' | 'created_at' | 'current_price' | 'last_updated'>) => 
    api.post<Asset>('/assets/', data),
  updatePrices: () => api.post('/assets/update-prices'),
};

export const holdingApi = {
  getAll: (portfolioId?: number) => {
    const params = portfolioId ? { portfolio_id: portfolioId } : {};
    return api.get<Holding[]>('/holdings/', { params });
  },
  getById: (id: number) => api.get<Holding>(`/holdings/${id}`),
  create: (data: Omit<Holding, 'id' | 'created_at' | 'updated_at' | 'asset'>) => 
    api.post<Holding>('/holdings/', data),
  update: (id: number, data: Partial<Holding>) => 
    api.put<Holding>(`/holdings/${id}`, data),
  delete: (id: number) => api.delete(`/holdings/${id}`),
};

export const transactionApi = {
  getAll: (portfolioId?: number) => {
    const params = portfolioId ? { portfolio_id: portfolioId } : {};
    return api.get<Transaction[]>('/transactions/', { params });
  },
  getById: (id: number) => api.get<Transaction>(`/transactions/${id}`),
  create: (data: Omit<Transaction, 'id' | 'created_at' | 'asset'>) => 
    api.post<Transaction>('/transactions/', data),
  update: (id: number, data: Partial<Transaction>) => 
    api.put<Transaction>(`/transactions/${id}`, data),
  delete: (id: number) => api.delete(`/transactions/${id}`),
};

export default api;