import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-800 py-4 z-10 px-6">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">FinAI</Link>
        <div className="space-x-6">
          <Link to="/" className="hover:text-blue-400">Home</Link>
          <Link to="/dashboard" className="hover:text-blue-400">Dashboard</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
