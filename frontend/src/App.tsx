import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Portfolios from './pages/Portfolios';
import Assets from './pages/Assets';
import Transactions from './pages/Transactions';
import HistoricalData from './pages/HistoricalData';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/portfolios" element={<Portfolios />} />
          <Route path="/assets" element={<Assets />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/historical" element={<HistoricalData />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
