import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import LandingPage from './LandingPage';
import DashboardPage from './Dashboard';
import UploadModal from './UploadModal';

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage setIsModalOpen={setIsModalOpen} />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
        <UploadModal isOpen={isModalOpen} setIsOpen={setIsModalOpen} />
      </div>
    </Router>
  );
}
export default App;