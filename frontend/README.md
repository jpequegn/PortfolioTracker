# Portfolio Tracker Frontend

A modern React TypeScript frontend for the Portfolio Tracker application, providing a comprehensive interface for managing investment portfolios, tracking performance, and analyzing diversification.

## Features

### 📊 Dashboard
- Portfolio performance overview with real-time metrics
- Interactive charts showing holdings performance
- Asset allocation and diversification analysis
- Portfolio selector for multi-portfolio management

### 💼 Portfolio Management
- Create, edit, and delete portfolios
- Portfolio metadata management
- Grid view with portfolio cards

### 📈 Asset Management
- View all available assets (stocks, bonds, ETFs, cash)
- Add new assets with automatic price fetching
- Search and filter assets
- Real-time price updates from Yahoo Finance
- Asset type categorization with color coding

### 💰 Transaction Management
- Record buy/sell transactions
- Support for multiple transaction types (buy, sell, dividend, split, deposit, withdrawal)
- Automatic total calculation
- Portfolio and asset filtering
- Transaction history with detailed information

### 🎨 Modern UI/UX
- Clean, responsive design with Tailwind CSS
- Interactive charts and visualizations using Recharts
- Loading states and error handling
- Mobile-friendly responsive layout
- Intuitive navigation with sidebar

## Technology Stack

- **React 18** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Axios** for API communication
- **Lucide React** for icons

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Portfolio Tracker backend running on `http://localhost:12000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view the application

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:12000/api/v1
PORT=3000
```

## Available Scripts

### `npm start`
Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `npm test`
Launches the test runner in interactive watch mode.

### `npm run build`
Builds the app for production to the `build` folder.

### `npm run eject`
**Note: this is a one-way operation. Once you `eject`, you can't go back!**

## Project Structure

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Layout.tsx      # Main layout with sidebar
│   │   ├── LoadingSpinner.tsx
│   │   └── PerformanceCard.tsx
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── Portfolios.tsx  # Portfolio management
│   │   ├── Assets.tsx      # Asset management
│   │   └── Transactions.tsx # Transaction management
│   ├── services/           # API service layer
│   │   └── api.ts          # API client and types
│   ├── App.tsx             # Main app component
│   └── index.tsx           # Entry point
├── tailwind.config.js      # Tailwind configuration
└── package.json
```

## Integration with Backend

The frontend is designed to work seamlessly with the Portfolio Tracker backend:

- **Real-time data** fetching and updates
- **Automatic price synchronization**
- **Transaction processing** with holding updates
- **Performance calculations** with live data

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).