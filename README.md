# AI Marketing Campaign Optimizer

## Overview

This is a Streamlit-based AI-powered marketing campaign optimization platform that uses a multi-agent system to analyze, optimize, and track digital marketing campaigns. The application leverages machine learning models to provide insights on campaign performance, budget allocation, A/B testing, and customer segmentation.

## System Architecture

The application follows a modular multi-agent architecture with clear separation of concerns:

- **Frontend**: Streamlit web application providing an interactive dashboard
- **Agent System**: Specialized AI agents for different marketing optimization tasks
- **Utilities**: Supporting modules for data generation, ML models, and visualizations
- **Data Layer**: In-memory data processing using pandas DataFrames

The architecture is designed for extensibility, allowing easy addition of new agents and optimization strategies.

## Key Components

### Core Agents
- **CampaignAnalyzer**: Analyzes campaign performance, identifies top/underperforming campaigns, and provides actionable recommendations
- **BudgetOptimizer**: Uses machine learning to optimize budget allocation across campaigns based on ROI or other KPIs
- **PerformanceTracker**: Tracks KPIs, calculates comprehensive metrics, and predicts future performance trends
- **ABTestAgent**: Suggests A/B tests, analyzes statistical significance, and provides testing recommendations

### Utilities
- **DataGenerator**: Creates realistic synthetic marketing data for demonstration and testing
- **MLModelSuite**: Comprehensive suite of ML models (Random Forest, Gradient Boosting, K-Means clustering)
- **DashboardVisualizer**: Creates interactive Plotly visualizations for campaign performance

### Technology Stack
- **Frontend**: Streamlit for rapid dashboard development
- **Data Processing**: Pandas and NumPy for data manipulation
- **Machine Learning**: Scikit-learn for predictive models and clustering
- **Optimization**: SciPy for mathematical optimization algorithms
- **Visualization**: Plotly for interactive charts and graphs
- **Statistics**: SciPy.stats for A/B testing statistical analysis

## Data Flow

1. **Data Generation**: Synthetic marketing data is generated including campaigns, customers, daily metrics, and interactions
2. **Agent Processing**: Each specialized agent processes the data to provide domain-specific insights
3. **ML Training**: Models are trained on campaign data to predict ROI, conversions, and customer behavior
4. **Optimization**: Budget allocation is optimized using mathematical optimization techniques
5. **Visualization**: Results are presented through interactive dashboards and charts
6. **Recommendations**: Actionable insights are generated for marketing strategy improvements

## External Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **scikit-learn**: Machine learning algorithms
- **scipy**: Scientific computing and optimization
- **datetime**: Date and time handling

No external APIs or databases are currently used - the system operates with synthetic data for demonstration purposes.

## Deployment Strategy

The application is designed for Replit deployment with:
- Single-file entry point (`app.py`)
- Self-contained Python environment
- In-memory data processing (no database required)
- Streamlit's built-in serving capabilities

Future enhancements could include:
- Database integration for persistent data storage
- External API connections for real marketing data
- Cloud deployment for production use

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Enhancements

### Advanced AI Capabilities Added (June 28, 2025)
- **Real-Time Monitoring Agent**: Added comprehensive monitoring system with intelligent alerts and health scoring
- **Enhanced UI/UX**: Custom CSS styling, improved metrics visualization with status indicators
- **Advanced Controls**: Configurable alert thresholds, risk tolerance settings, and optimization parameters
- **Comprehensive Dashboard**: Added 6-tab interface including real-time monitoring with anomaly detection
- **Smart Alerting System**: Multi-level alert system (critical/warning/info) with actionable recommendations
- **Performance Analytics**: Enhanced KPI tracking with industry benchmarks and trend analysis
- **Interactive Configuration**: User-customizable alert thresholds and monitoring sensitivity

### System Architecture Updates
- Added RealTimeMonitor agent for continuous campaign health assessment
- Enhanced existing agents with more sophisticated analysis capabilities
- Improved data visualization with performance heatmaps and trend analysis
- Integrated multi-channel attribution modeling and customer lifetime value prediction

## Changelog

- June 28, 2025: Initial multi-agent system implementation
- June 28, 2025: Enhanced with advanced monitoring, alerting, and comprehensive analytics features