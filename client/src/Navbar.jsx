import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-gray-800/80 backdrop-blur-sm py-4 px-6 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center text-2xl font-bold  "><svg fill="#ffffff" height="40px" width="40px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 386.651 386.651" xml:space="preserve" stroke="#ffffff"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M342.367,135.781c-2.674-1.367-5.889-1.122-8.324,0.635l-138.556,99.968l-89.233-83.725 c-3.032-2.844-7.736-2.892-10.826-0.112l-74.395,66.959c-1.685,1.518-2.648,3.679-2.648,5.946v91.451c0,4.418,3.582,8,8,8h312.339 c4.418,0,8-3.582,8-8v-174C346.724,139.899,345.041,137.149,342.367,135.781z M53.507,308.903H34.385v-79.889l19.122-17.211 V308.903z M88.045,308.903H69.507v-111.5l18.538-16.685V308.903z M122.582,308.903h-18.538V172.526l18.538,17.393V308.903z M157.12,308.903h-18.538V204.931l18.538,17.394V308.903z M192.015,308.903H173.12v-71.565l16.227,15.226 c0.791,0.741,1.702,1.288,2.667,1.65V308.903z M226.91,308.903h-18.896v-61.828l18.896-13.634V308.903z M261.806,308.903H242.91 v-87.006l18.895-13.633V308.903z M296.701,308.903h-18.896V196.72l18.896-13.634V308.903z M330.724,308.903h-18.022v-137.36 l18.022-13.003V308.903z"></path> <path d="M385.375,65.087c-1.439-2.148-3.904-3.404-6.461-3.337l-50.696,1.368c-3.471,0.094-6.429,2.547-7.161,5.941 c-0.732,3.395,0.95,6.85,4.074,8.366l11.846,5.75L196.96,183.012l-95.409-86.504c-4.738-4.296-11.955-4.322-16.723-0.062 L4.173,168.491c-5.149,4.599-5.594,12.501-0.995,17.649c4.598,5.148,12.499,5.594,17.649,0.995l72.265-64.55l94.533,85.709 c2.369,2.147,5.376,3.239,8.398,3.239c2.532,0,5.074-0.767,7.255-2.322L350.82,104.01l0.701,11.074 c0.22,3.464,2.777,6.329,6.193,6.939c0.444,0.079,0.889,0.118,1.328,0.118c2.938,0,5.662-1.724,6.885-4.483l20.077-45.327 C387.052,69.968,386.815,67.234,385.375,65.087z"></path> </g> </g></svg>FinAllytics</Link>
        <div className="space-x-12">
          <Link to="/" className="hover:text-blue-400 text-1xl" style={{
                  fontFamily: "Manrope, sans-serif",
                  fontWeight:400,
                  fontSize:18,
                }}>Home</Link>
          <Link to="/dashboard" className="hover:text-blue-400 text-1xl" style={{
                  fontFamily: "Manrope, sans-serif",
                  fontWeight:400,
                  fontSize:18,
                }}>Dashboard</Link>
        </div>
        <div className="Login">
          {/* "Start Now" button */}
          <Link to="/start" className="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition duration-300">
            Start Now
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
