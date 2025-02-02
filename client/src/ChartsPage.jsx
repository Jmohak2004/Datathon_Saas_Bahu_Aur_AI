import React, { useState } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, AreaChart, Area } from 'recharts';
import './charts.css';

const ChartsPage = () => {
  const [companyName, setCompanyName] = useState('');
  const [data, setData] = useState(null);

  // Generate random data based on company name
  const generateMockData = (name) => {
    const seed = Array.from(name).reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const random = (min, max) => Math.floor((seed * Math.random() * (max - min + 1)) + min);

    // Revenue distribution data
    const revenueData = [
      { name: 'Product Sales', value: random(30, 50) },
      { name: 'Services', value: random(20, 40) },
      { name: 'Subscriptions', value: random(15, 30) },
      { name: 'Other', value: random(5, 15) }
    ];

    // Monthly sales data
    const monthlyData = Array.from({ length: 12 }, (_, i) => ({
      month: new Date(2024, i).toLocaleString('default', { month: 'short' }),
      sales: random(50000, 150000),
      growth: random(-5, 15)
    }));

    // Customer age distribution
    const ageData = Array.from({ length: 6 }, (_, i) => ({
      age: '${20 + i * 10}-${29 + i * 10}',
      customers: random(1000, 5000)
    }));

    return {
      revenueData,
      monthlyData,
      ageData
    };
  };

  const handleGenerate = () => {
    if (companyName.trim()) {
      const mockData = generateMockData(companyName);
      setData(mockData);
    }
  };

  const generateAnalysis = (data) => {
    if (!data) return '';

    const totalRevenue = data.revenueData.reduce((acc, item) => acc + item.value, 0);
    const maxGrowth = Math.max(...data.monthlyData.map(item => item.growth));
    const avgCustomerAge = data.ageData.reduce((acc, item) => {
      const midAge = parseInt(item.age.split('-')[0]) + 5;
      return acc + (midAge * item.customers);
    }, 0) / data.ageData.reduce((acc, item) => acc + item.customers, 0);

    return `
      Based on the analysis of ${companyName}'s data:
      - The company's revenue is primarily driven by ${data.revenueData[0].name} at ${data.revenueData[0].value}% of total revenue
      - Peak growth was observed at ${maxGrowth.toFixed(1)}%
      - The average customer age is approximately ${avgCustomerAge.toFixed(1)} years
    `;
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="dashboard-container">
      <div className="input-section">
        <h1>Company Analysis Dashboard</h1>
        <div className="input-group">
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="Enter company name"
          />
          <button onClick={handleGenerate}>Generate Analysis</button>
        </div>
      </div>

      {data && (
        <div className="dashboard-content">
          <h2>{companyName} Analysis</h2>
          
          <div className="charts-grid">
            <div className="chart-container">
              <h3>Revenue Distribution</h3>
              <PieChart width={300} height={300}>
              <Pie
  data={data.revenueData}
  cx={150}
  cy={150}
  innerRadius={60}
  outerRadius={80}
  fill="#8884d8"
  dataKey="value"
  label
>
  {data.revenueData.map((entry, index) => (
    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
  ))}
</Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </div>

            <div className="chart-container">
              <h3>Monthly Sales Growth</h3>
              <BarChart width={400} height={300} data={data.monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="growth" fill="#8884d8" />
              </BarChart>
            </div>

            <div className="chart-container">
              <h3>Customer Age Distribution</h3>
              <AreaChart width={400} height={300} data={data.ageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="age" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="customers" stroke="#8884d8" fill="#8884d8" />
              </AreaChart>
            </div>
          </div>

          <div className="analysis-section">
            <h3>Analysis & Insights</h3>
            <p>{generateAnalysis(data)}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChartsPage;