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

## Changelog

Changelog:
- June 28, 2025. Initial setup