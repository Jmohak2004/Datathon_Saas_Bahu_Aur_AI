import { WavyBackground } from "./wavy-background"

function LandingPage({ setIsModalOpen }) {
  return (
    <main className="relative min-h-screen bg-gray-900 text-white">
      <WavyBackground className="max-w-4xl mx-auto">
        <div className="max-w-7xl w-full px-6 pt-24">
          <div className="text-center space-y-12">
            <h1 className="text-5xl md:text-6xl font-bold leading-tight md:leading-tight">
              <span
                className="text-transparent"
                style={{
                  fontFamily: "Manrope, sans-serif",
                  fontStyle: "normal",
                  fontWeight: 700,
                  background: "linear-gradient(180deg, #fff, #ffffff4f)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  textWrap: "balance",
                }}
              >
                Revolutionize Financial Reporting
                <br />
                with Artificial Intelligence
              </span>
            </h1>

            <p
              className="text-xl md:text-2xl text-gray-300 max-w-2xl mx-auto leading-relaxed"
              style={{
                fontFamily: "Manrope, sans-serif",
              }}
            >
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

      {/* Introduction Section */}
      <section className="py-20 bg-gray-800">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold mb-8 text-center">Welcome to the Future of Financial Narratives</h2>
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <p className="text-xl leading-relaxed mb-4">
                Our AI-powered system generates financial reports and narratives that are accurate, coherent, and
                data-driven. Say goodbye to misinformation and hello to reliable insights.
              </p>
            </div>
            <div className="md:w-1/2">
              <img
                src="/placeholder.svg?height=300&width=400"
                alt="Financial data analysis"
                className="rounded-lg shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-900">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold mb-12 text-center">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { title: "Data Analysis", description: "Analyze vast amounts of financial data for accurate insights." },
              { title: "Market Trends", description: "Stay updated with the latest market trends and sentiments." },
              {
                title: "Probabilistic Consistency",
                description: "Ensure logical consistency and reliability in every report.",
              },
              { title: "Customizable Reports", description: "Generate tailored reports to meet your specific needs." },
              {
                title: "Visualization Tools",
                description: "Enhance your reports with charts, graphs, and visual aids.",
              },
            ].map((feature, index) => (
              <div key={index} className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-2xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-800">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold mb-12 text-center">How It Works</h2>
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <ol className="list-decimal list-inside space-y-4">
                <li className="text-xl">
                  <span className="font-semibold">Data Collection:</span> Gather financial data, market trends, and
                  historical patterns.
                </li>
                <li className="text-xl">
                  <span className="font-semibold">Analysis:</span> Use advanced algorithms to analyze and interpret the
                  data.
                </li>
                <li className="text-xl">
                  <span className="font-semibold">Report Generation:</span> Generate coherent and insightful financial
                  narratives.
                </li>
                <li className="text-xl">
                  <span className="font-semibold">Validation:</span> Ensure accuracy and logical consistency through
                  expert reviews.
                </li>
              </ol>
            </div>
            <div className="md:w-1/2">
              <img
                src="/placeholder.svg?height=300&width=400"
                alt="Process flowchart"
                className="rounded-lg shadow-xl"
              />
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

