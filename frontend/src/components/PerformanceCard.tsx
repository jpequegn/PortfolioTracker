import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface PerformanceCardProps {
  title: string;
  value: string;
  change?: number;
  changePercent?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
}

const PerformanceCard: React.FC<PerformanceCardProps> = ({
  title,
  value,
  change,
  changePercent,
  prefix = '',
  suffix = '',
  className = '',
}) => {
  const isPositive = change ? change >= 0 : changePercent ? changePercent >= 0 : true;
  const changeValue = change || changePercent;

  return (
    <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">
            {prefix}{value}{suffix}
          </p>
        </div>
        {changeValue !== undefined && (
          <div className={`flex items-center ${isPositive ? 'text-success-600' : 'text-danger-600'}`}>
            {isPositive ? (
              <TrendingUp className="h-4 w-4 mr-1" />
            ) : (
              <TrendingDown className="h-4 w-4 mr-1" />
            )}
            <span className="text-sm font-medium">
              {isPositive ? '+' : ''}{changeValue?.toFixed(2)}
              {changePercent !== undefined ? '%' : ''}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default PerformanceCard;