import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function DashboardPage() {
  const data = [
    { month: 'Jan', revenue: 4000, expenses: 2400 },
    { month: 'Feb', revenue: 3000, expenses: 1398 },
    { month: 'Mar', revenue: 2000, expenses: 9800 },
    { month: 'Apr', revenue: 2780, expenses: 3908 },
  ];

  const templates = [
    { id: 1, name: 'Annual Financial Report' },
    { id: 2, name: 'Quarterly Performance Analysis' },
    { id: 3, name: 'Cash Flow Statement' },
    { id: 4, name: 'Balance Sheet' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <h1 className="text-3xl font-bold mb-8">Financial Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-4">Revenue vs Expenses</h2>
          <LineChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
            <Line type="monotone" dataKey="expenses" stroke="#82ca9d" />
          </LineChart>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-4">Report Templates</h2>
          <div className="space-y-4">
            {templates.map((template) => (
              <div
                key={template.id}
                className="p-4 bg-gray-700 rounded-lg hover:bg-gray-600 cursor-pointer transition-colors"
              >
                {template.name}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;