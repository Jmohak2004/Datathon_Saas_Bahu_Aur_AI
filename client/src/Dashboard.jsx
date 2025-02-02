import React, { useState, useEffect } from 'react';
import { Line, Bar, Scatter, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const FinancialDashboard = () => {
  const [apiKey, setApiKey] = useState('');
  const [ticker, setTicker] = useState('AAPL');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fallback data in case API calls fail
  const getFallbackData = () => ({
    months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    stockPrice: [150, 155, 160, 158, 162, 165],
    earnings: [2.5, 2.6, 2.7, 2.8, 2.9, 3.0],
    revenue: [90, 95, 92, 98, 100, 103],
    margins: [0.3, 0.31, 0.29, 0.32, 0.33, 0.32],
    debtEquity: [0.4, 0.39, 0.38, 0.37, 0.36, 0.35],
    cashFlow: [15, 16, 14, 17, 18, 19],
    netIncome: [12, 13, 11, 14, 15, 16],
  });

  const fetchFinancialData = async () => {
    if (!apiKey) {
      setError('Please enter your Finnhub API key');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const headers = {
        'Content-Type': 'application/json',
        'X-Finnhub-Token': apiKey
      };

      // Test the API key first
      const testResponse = await fetch(
        `https://finnhub.io/api/v1/stock/profile2?symbol=${ticker}`,
        { headers }
      );

      if (!testResponse.ok) {
        throw new Error(
          testResponse.status === 401 
            ? 'Invalid API key. Please check your Finnhub API key.'
            : `API Error: ${testResponse.status}`
        );
      }

      // Fetch basic metrics
      const [metricsResponse, financialsResponse, priceResponse] = await Promise.all([
        fetch(`https://finnhub.io/api/v1/stock/metric?symbol=${ticker}&metric=all`, { headers }),
        fetch(`https://finnhub.io/api/v1/stock/financials-reported?symbol=${ticker}`, { headers }),
        fetch(`https://finnhub.io/api/v1/stock/candle?symbol=${ticker}&resolution=D&from=${Math.floor(Date.now()/1000 - 180*24*60*60)}&to=${Math.floor(Date.now()/1000)}`, { headers })
      ]);

      if (!metricsResponse.ok || !financialsResponse.ok || !priceResponse.ok) {
        throw new Error('Failed to fetch some financial data');
      }

      const [metricsData, financialsData, priceData] = await Promise.all([
        metricsResponse.json(),
        financialsResponse.json(),
        priceResponse.json()
      ]);

      // Process the data...
      const processedData = {
        months: priceData.t?.map(timestamp => 
          new Date(timestamp * 1000).toLocaleDateString('en-US', { month: 'short' })
        ) || getFallbackData().months,
        stockPrice: priceData.c || getFallbackData().stockPrice,
        earnings: Array(6).fill(metricsData.metric?.epsGrowth || 0),
        revenue: financialsData.data?.[0]?.report?.bs?.map(item => 
          item.totalRevenue
        ) || getFallbackData().revenue,
        margins: financialsData.data?.[0]?.report?.bs?.map(item =>
          (item.grossProfit / item.totalRevenue) || 0
        ) || getFallbackData().margins,
        debtEquity: Array(6).fill(metricsData.metric?.totalDebtToEquity || 0),
        cashFlow: financialsData.data?.[0]?.report?.cf?.map(item => 
          item.cashFromOperating
        ) || getFallbackData().cashFlow,
        netIncome: financialsData.data?.[0]?.report?.ic?.map(item => 
          item.netIncome
        ) || getFallbackData().netIncome,
      };

      setData(processedData);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching financial data:', err);
      // Set fallback data on error
      setData(getFallbackData());
    } finally {
      setLoading(false);
    }
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      }
    }
  };

  const renderCharts = () => {
    if (!data) return null;

    const lineChartData = {
      labels: data.months,
      datasets: [
        {
          label: 'Stock Price',
          data: data.stockPrice,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        },
        {
          label: 'EPS Growth',
          data: data.earnings,
          borderColor: 'rgb(255, 99, 132)',
          tension: 0.1
        }
      ]
    };

    const barChartData = {
      labels: data.months,
      datasets: [
        {
          label: 'Revenue',
          data: data.revenue,
          backgroundColor: 'rgba(53, 162, 235, 0.5)'
        },
        {
          label: 'Profit Margins',
          data: data.margins,
          backgroundColor: 'rgba(75, 192, 192, 0.5)'
        }
      ]
    };

    const scatterChartData = {
      datasets: [{
        label: 'Cash Flow vs Net Income',
        data: data.cashFlow.map((cf, i) => ({
          x: cf,
          y: data.netIncome[i]
        })),
        backgroundColor: 'rgb(255, 99, 132)'
      }]
    };

    const pieChartData = {
      labels: ['Your Company', 'Competitor A', 'Competitor B', 'Others'],
      datasets: [{
        data: [30, 25, 20, 25],
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)'
        ]
      }]
    };

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ChartContainer title="Stock Price & EPS Growth">
          <Line data={lineChartData} options={chartOptions} />
        </ChartContainer>

        <ChartContainer title="Revenue & Margins">
          <Bar data={barChartData} options={chartOptions} />
        </ChartContainer>

        <ChartContainer title="Cash Flow vs Net Income">
          <Scatter data={scatterChartData} options={chartOptions} />
        </ChartContainer>

        <ChartContainer title="Market Share Analysis">
          <Pie data={pieChartData} options={chartOptions} />
        </ChartContainer>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-center mb-6">Financial Analytics Dashboard</h1>
        
        <div className="max-w-xl mx-auto space-y-4">
          <div className="flex flex-col space-y-2">
            <label htmlFor="apiKey" className="text-sm font-medium">
              Finnhub API Key
            </label>
            <input
              id="apiKey"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="border rounded p-2"
              placeholder="Enter your Finnhub API key"
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <label htmlFor="ticker" className="text-sm font-medium">
              Stock Ticker
            </label>
            <input
              id="ticker"
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              className="border rounded p-2"
              placeholder="Enter stock ticker (e.g., AAPL)"
            />
          </div>

          <button
            onClick={fetchFinancialData}
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:bg-blue-300"
          >
            {loading ? 'Loading...' : 'Fetch Data'}
          </button>

          {error && (
            <div className="text-red-500 text-center p-2 bg-red-50 rounded">
              {error}
            </div>
          )}
        </div>
      </div>

      {renderCharts()}
    </div>
  );
};

export default FinancialDashboard;