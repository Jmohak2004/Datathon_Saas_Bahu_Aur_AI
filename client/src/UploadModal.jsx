import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UploadModal({ isOpen, setIsOpen }) {
  const [companyName, setCompanyName] = useState('');
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle file upload and company name
    navigate('/dashboard');
    setIsOpen(false);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-gray-800 rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6">Get Started</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block mb-2">Company Name</label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600"
              required
            />
          </div>
          <div>
            <label className="block mb-2">Upload Financial Data</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600"
              required
            />
          </div>
          <div className="flex space-x-4">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded flex-1"
            >
              Submit
            </button>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default UploadModal;
