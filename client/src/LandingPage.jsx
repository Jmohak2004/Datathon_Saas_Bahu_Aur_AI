import { WavyBackground } from "./wavy-background";
import React from "react";

function LandingPage({ setIsModalOpen }) {
  return (
    <>
      <div className="min-h-[calc(100vh-64px)] flex items-center justify-center">
        <WavyBackground className="max-w-4xl mx-auto pb-40">
        <div className="max-w-7xl w-full px-6">
          <div className="text-center space-y-12">  
            <h1 className="text-5xl md:text-6xl font-bold leading-tight md:leading-tight">
              <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Revolutionize Financial Reporting
                <br className="md:block" />
                with Artificial Intelligence
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
              Accurate, Data-Driven Financial Insights with Probabilistic Consistency
            </p>
            
            <div className="pt-4">
              <button
                onClick={() => setIsModalOpen(true)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-10 py-4 rounded-lg text-xl font-semibold transition-all duration-200 hover:transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
        </WavyBackground>
      </div>
      </>
  );
}

export default LandingPage;