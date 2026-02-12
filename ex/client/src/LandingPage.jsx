import { WavyBackground } from "./wavy-background"
import React from 'react';
import { ArrowRight } from 'lucide-react';
import { StarsBackground } from "./stars-background";


const FeatureCard = ({ icon, title, description, delay }) => (
  <div 
    className="bg-neutral-900 p-6 rounded-xl border border-neutral-700 hover:border-blue-500 transition-all duration-300 animate-fadeIn"
    style={{ animationDelay: delay }}
  >
    <div className={`flex items-center justify-center w-12 h-12 rounded-lg ${
      title.includes('Predictive') || title.includes('Visualized') || title.includes('API') 
        ? 'bg-cyan-500/10' 
        : 'bg-blue-500/10'
    } mb-6`}>
      {icon}
    </div>
    <h3 className="text-xl font-semibold text-white mb-3">{title}</h3>
    <p className="text-gray-400">{description}</p>
  </div>
);
const Button = ({ children, variant = "default", size = "default", className = "" }) => {
  const baseStyles = "inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50";
  
  const variants = {
    default: "bg-primary text-primary-foreground hover:opacity-90",
    outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground"
  };
  
  const sizes = {
    default: "h-10 px-4 py-2",
    lg: "h-11 rounded-md px-8"
  };
  
  return (
    <button className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}>
      {children}
    </button>
  );
};

function LandingPage({ setIsModalOpen }) {
  const features = [
    {
      title: "Smart Data Processing",
      description: "Extracts and analyzes real-time market data with advanced AI algorithms for precise insights.",
      icon: (
        <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
        </svg>
      ),
    },
    {
      title: "Predictive Insights",
      description: "Uses AI to forecast trends and identify opportunities in the market with high accuracy.",
      icon: (
        <svg className="w-6 h-6 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
        </svg>
      ),
    },
    {
      title: "Accuracy & Consistency",
      description: "Ensures probabilistic consistency with advanced validation mechanisms to prevent misinformation.",
      icon: (
        <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      title: "Visualized Reports",
      description: "Generates beautiful charts and graphs for better understanding of complex financial data.",
      icon: (
        <svg className="w-6 h-6 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
        </svg>
      ),
    },
    {
      title: "Real-Time Updates",
      description: "Integrates with stock APIs to provide up-to-date analysis and market insights.",
      icon: (
        <svg className="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
    },
    {
      title: "API Integration",
      description: "Seamlessly connect with existing financial systems through our robust API infrastructure.",
      icon: (
        <svg className="w-6 h-6 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      ),
    },
  ];

  return (
    <main className="relative min-h-screen bg-gray-900 text-white">
      <StarsBackground />
      <WavyBackground className="max-w-4xl mx-auto">
      <section className="container flex min-h-[calc(100vh-3.5rem)] max-w-screen-2xl mt-14 flex-col items-center justify-center space-y-8 py-24 text-center md:py-32">
      <div className="space-y-12">
      <button className="p-[3px] relative">
  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
  <div className="px-8 py-2  bg-black rounded-[6px]  relative group transition duration-200 text-white text-1xl  font-semibold">
  Comprehensive 11-Metric Financial Analysis
  </div>
</button><div>
        <h1 className="bg-gradient-to-b from-neutral-800 via-neutral-700 to-neutral-700 dark:from-neutral-800 dark:via-white dark:to-white bg-clip-text text-4xl  font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl">
     Financial Reporting 
        </h1>
        <h1 className="bg-gradient-to-b from-neutral-800 via-neutral-700 to-neutral-700 dark:from-neutral-800 dark:via-white dark:to-white bg-clip-text text-4xl  font-bold tracking-tight text-transparent sm:text-5xl md:text-6xl lg:text-7xl">
     Completely Revolutionized
        </h1>
        </div>
        <p className="dark:text-white text-black text-2xl leading-snug tracking-wide">
        Transform raw financial data into coherent, insightful, and reliable reports with cutting-edge AI and probabilistic consistency
        </p>
      </div>

                <button onClick={() => setIsModalOpen(true)} className="bg-slate-800 no-underline group cursor-pointer relative shadow-2xl shadow-zinc-900 rounded-full p-px text-base font-semibold leading-6 text-white inline-block">
  <span className="absolute inset-0 overflow-hidden rounded-full">
    <span className="absolute inset-0 rounded-full bg-[image:radial-gradient(75%_100%_at_50%_0%,rgba(56,189,248,0.6)_0%,rgba(56,189,248,0)_75%)] opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
  </span>
  <div className="relative flex space-x-2 items-center z-10 rounded-full bg-zinc-950 py-3 px-8 ring-1 ring-white/10 ">
    <span>
      Start Now
    </span>
    <svg
      fill="none"
      height="24"  
      viewBox="0 0 24 24"
      width="24"  
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M10.75 8.75L14.25 12L10.75 15.25"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
      />
    </svg>
  </div>
  <span className="absolute -bottom-0 left-[1.125rem] h-px w-[calc(100%-2.25rem)] bg-gradient-to-r from-emerald-400/0 via-emerald-400/90 to-emerald-400/0 transition-opacity duration-500 group-hover:opacity-40" />
</button>


    </section>
      </WavyBackground>

      {/* Features Section */}
      <section id="features" className="py-20 bg-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 animate-fadeIn">
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent mb-4">
            Powerful Features for Financial Analysis
          </h2>
          <p className="text-gray-400 text-2xl max-w-2xl mx-auto">
            Experience cutting-edge AI technology that transforms your financial data into actionable insights
          </p>
        </div>

        {/* Changed grid-cols-2 to grid-cols-3 for larger screens */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={feature.title}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={`${index * 0.2}s`}
            />
          ))}
        </div>
      </div>
    </section>

      {/* How It Works Section */}
      <section id="howitworks" className="py-20 bg-neutral-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16 animate__animated animate__fadeIn">
          <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent mb-4">
            How Our Model Works
          </h2>
          <p className="text-gray-400 text-2xl max-w-2xl mx-auto">
            A sophisticated process that ensures accuracy and reliability at every step
          </p>
        </div>

        {/* Timeline Steps */}
        <div className="relative">
          {/* Connection Line */}
          <div className="hidden md:block absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-gradient-to-b from-blue-500 to-cyan-500 opacity-20"></div>

          {/* Steps */}
          <div className="space-y-16">
            {/* Step 1 */}
            <div className="relative flex items-center justify-center md:justify-between animate__animated animate__fadeInLeft">
              <div className="hidden md:block w-5/12 text-right pr-8">
                <h3 className="text-xl font-semibold text-white mb-2">Data Collection & Preprocessing</h3>
                <p className="text-gray-400">Scrapes and processes real-time financial data from multiple trusted sources</p>
              </div>
              <div className="absolute md:static flex items-center justify-center">
                <div className="w-12 h-12 bg-neutral-800 rounded-full border-4 border-blue-500 flex items-center justify-center z-10">
                  <span className="text-blue-500 font-bold">1</span>
                </div>
              </div>
              <div className="md:w-5/12 md:pl-8">
                <div className="md:hidden mb-4">
                  <h3 className="text-xl font-semibold text-white mb-2">Data Collection & Preprocessing</h3>
                </div>
                <div className="bg-neutral-800 p-6 rounded-xl border border-neutral-700">
                  <div className="flex items-center space-x-4">
                    <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
                    </svg>
                    <span className="text-gray-300">Real-time data processing</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative flex items-center justify-center md:justify-between animate__animated animate__fadeInRight">
              <div className="md:w-5/12 text-right pr-8">
                <div className="bg-neutral-800 p-6 rounded-xl border border-neutral-700">
                  <div className="flex items-center justify-end space-x-4">
                    <span className="text-gray-300">Advanced AI predictions</span>
                    <svg className="w-8 h-8 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                </div>
              </div>
              <div className="absolute md:static flex items-center justify-center">
                <div className="w-12 h-12 bg-neutral-800 rounded-full border-4 border-cyan-500 flex items-center justify-center z-10">
                  <span className="text-cyan-500 font-bold">2</span>
                </div>
              </div>
              <div className="md:w-5/12 pl-8">
                <h3 className="text-xl font-semibold text-white mb-2">Trend Analysis & Forecasting</h3>
                <p className="text-gray-400">Uses AI models for accurate stock predictions and trend analysis</p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative flex items-center justify-center md:justify-between animate__animated animate__fadeInLeft">
              <div className="hidden md:block w-5/12 text-right pr-8">
                <h3 className="text-xl font-semibold text-white mb-2">Narrative Generation</h3>
                <p className="text-gray-400">Generates insightful and coherent narratives based on financial data</p>
              </div>
              <div className="absolute md:static flex items-center justify-center">
                <div className="w-12 h-12 bg-neutral-800 rounded-full border-4 border-blue-500 flex items-center justify-center z-10">
                  <span className="text-blue-500 font-bold">3</span>
                </div>
              </div>
              <div className="md:w-5/12 md:pl-8">
                <div className="md:hidden mb-4">
                  <h3 className="text-xl font-semibold text-white mb-2">Narrative Generationx`</h3>
                </div>
                <div className="bg-neutral-800 p-6 rounded-xl border border-neutral-700">
                  <div className="flex items-center space-x-4">
                    <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    <span className="text-gray-300">AI-driven content creation for detailed reports</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Step 4 */}
            <div className="relative flex items-center justify-center md:justify-between animate__animated animate__fadeInRight">
              <div className="md:w-5/12 text-right pr-8">
                <div className="bg-neutral-800 p-6 rounded-xl border border-neutral-700">
                  <div className="flex items-center justify-end space-x-4">
                    <span className="text-gray-300">Ensures reliability and consistency in all financial statements</span>
                    <svg className="w-8 h-8 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                    </svg>
                  </div>
                </div>
              </div>
              <div className="absolute md:static flex items-center justify-center">
                <div className="w-12 h-12 bg-neutral-800 rounded-full border-4 border-cyan-500 flex items-center justify-center z-10">
                  <span className="text-cyan-500 font-bold">4</span>
                </div>
              </div>
              <div className="md:w-5/12 pl-8">
                <h3 className="text-xl font-semibold text-white mb-2">Fact-Checking & Validation</h3>
                <p className="text-gray-400">Verifies data accuracy through multiple trusted sources</p>
              </div>
            </div>

            {/* Step 5 */}
            <div className="relative flex items-center justify-center md:justify-between animate__animated animate__fadeInLeft">
              <div className="hidden md:block w-5/12 text-right pr-8">
                <h3 className="text-xl font-semibold text-white mb-2">Final Report Structuring</h3>
                <p className="text-gray-400">Organizes and formats data into clear, professional reports</p>
              </div>
              <div className="absolute md:static flex items-center justify-center">
                <div className="w-12 h-12 bg-neutral-800 rounded-full border-4 border-blue-500 flex items-center justify-center z-10">
                  <span className="text-blue-500 font-bold">5</span>
                </div>
              </div>
              <div className="md:w-5/12 md:pl-8">
                <div className="md:hidden mb-4">
                  <h3 className="text-xl font-semibold text-white mb-2">Final Report Structuring</h3>
                </div>
                <div className="bg-neutral-800 p-6 rounded-xl border border-neutral-700">
                  <div className="flex items-center space-x-4">
                    <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                    <span className="text-gray-300">Streamlined report generation for easy readability and understanding</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

      {/* Footer */}
      <footer className="bg-gray-900 py-8">
        <div className="container mx-auto px-6 text-center">
          <p className="text-gray-300">&copy; 2025 AI Financial Reporting. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

export default LandingPage

