import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import our custom modules
from agents.campaign_analyzer import CampaignAnalyzer
from agents.budget_optimizer import BudgetOptimizer
from agents.performance_tracker import PerformanceTracker
from agents.ab_test_agent import ABTestAgent
from agents.real_time_monitor import RealTimeMonitor
from utils.data_generator import DataGenerator
from utils.visualizations import DashboardVisualizer

# Configure page
st.set_page_config(
    page_title="AI Marketing Campaign Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #cce7ff;
        border: 1px solid #b3d9ff;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_generated' not in st.session_state:
    st.session_state.data_generated = False
if 'campaign_data' not in st.session_state:
    st.session_state.campaign_data = None

# Initialize agents and utilities
@st.cache_resource
def initialize_system():
    """Initialize the multi-agent system components"""
    data_gen = DataGenerator()
    campaign_analyzer = CampaignAnalyzer()
    budget_optimizer = BudgetOptimizer()
    performance_tracker = PerformanceTracker()
    ab_test_agent = ABTestAgent()
    real_time_monitor = RealTimeMonitor()
    visualizer = DashboardVisualizer()
    
    return data_gen, campaign_analyzer, budget_optimizer, performance_tracker, ab_test_agent, real_time_monitor, visualizer

def main():
    # Header with custom styling
    st.markdown('<h1 class="main-header">🚀 AI-Powered Marketing Campaign Optimizer</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent System for Digital Marketing Excellence")
    
    # Add introduction
    with st.expander("ℹ️ About This System", expanded=False):
        st.markdown("""
        **This comprehensive AI-powered marketing optimization platform features:**
        
        🤖 **AI Agents:**
        - **Campaign Analyzer**: Analyzes performance, identifies trends, provides actionable insights
        - **Budget Optimizer**: Uses machine learning to optimize budget allocation across campaigns
        - **Performance Tracker**: Tracks KPIs, predicts future performance with time series analysis
        - **A/B Test Agent**: Suggests experiments, analyzes statistical significance, provides testing roadmap
        
        📊 **Advanced Features:**
        - Real-time performance monitoring and alerts
        - Predictive analytics with confidence intervals
        - Customer segmentation and lifetime value prediction
        - Multi-channel attribution modeling
        - Automated budget reallocation recommendations
        
        🔬 **Machine Learning Models:**
        - Random Forest for ROI prediction
        - Gradient Boosting for conversion rate optimization
        - K-Means clustering for customer segmentation
        - Logistic Regression for churn prediction
        - Time series forecasting for performance trends
        """)
    
    # Initialize system components
    data_gen, campaign_analyzer, budget_optimizer, performance_tracker, ab_test_agent, real_time_monitor, visualizer = initialize_system()
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Data generation controls
        st.subheader("Data Configuration")
        num_campaigns = st.slider("Number of Campaigns", 5, 50, 20)
        num_customers = st.slider("Customer Base Size", 1000, 10000, 5000)
        date_range = st.slider("Campaign Duration (days)", 7, 90, 30)
        
        if st.button("🔄 Generate New Campaign Data", type="primary"):
            with st.spinner("Generating campaign data..."):
                st.session_state.campaign_data = data_gen.generate_campaign_data(
                    num_campaigns=num_campaigns,
                    num_customers=num_customers,
                    date_range=date_range
                )
                st.session_state.data_generated = True
                st.success("Data generated successfully!")
                st.rerun()
        
        # Agent controls
        st.subheader("🤖 AI Agents")
        auto_refresh = st.checkbox("Auto-refresh analytics", value=False)
        refresh_interval = 10  # Default value
        if auto_refresh:
            refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 10)
        
        # Advanced Settings
        st.subheader("⚙️ Advanced Settings")
        with st.expander("Model Configuration"):
            confidence_threshold = st.slider("Prediction Confidence Threshold", 0.6, 0.95, 0.8)
            enable_ml_training = st.checkbox("Enable ML Model Training", value=True)
            forecast_horizon = st.slider("Forecast Horizon (days)", 7, 90, 30)
    
    # Main content area
    if not st.session_state.data_generated:
        st.info("👈 Please generate campaign data using the sidebar controls to begin analysis.")
        return
    
    # Get campaign data
    campaign_data = st.session_state.campaign_data
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard Overview", 
        "🎯 Campaign Analysis", 
        "💰 Budget Optimization", 
        "📈 Performance Tracking", 
        "🧪 A/B Testing",
        "🚨 Real-Time Monitoring"
    ])
    
    with tab1:
        display_dashboard_overview(campaign_data, visualizer, performance_tracker)
    
    with tab2:
        display_campaign_analysis(campaign_data, campaign_analyzer, visualizer)
    
    with tab3:
        display_budget_optimization(campaign_data, budget_optimizer, visualizer)
    
    with tab4:
        display_performance_tracking(campaign_data, performance_tracker, visualizer)
    
    with tab5:
        display_ab_testing(campaign_data, ab_test_agent, visualizer)
    
    with tab6:
        display_real_time_monitoring(campaign_data, real_time_monitor, visualizer)
    
    # Auto-refresh functionality
    if auto_refresh and 'refresh_interval' in locals():
        time.sleep(refresh_interval)
        st.rerun()
    
    # Footer with system status
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("🤖 AI Agents: Active")
    with col2:
        st.caption("📊 ML Models: Ready")
    with col3:
        st.caption("⚡ System Status: Online")

def display_dashboard_overview(campaign_data, visualizer, performance_tracker):
    """Display the main dashboard overview"""
    st.header("📊 Campaign Dashboard Overview")
    
    # Calculate comprehensive metrics
    campaigns_df = campaign_data['campaigns']
    total_campaigns = len(campaigns_df)
    total_spend = campaigns_df['budget_spent'].sum()
    total_revenue = campaigns_df['revenue'].sum()
    total_conversions = campaigns_df['conversions'].sum()
    total_clicks = campaigns_df['clicks'].sum()
    total_impressions = campaigns_df['impressions'].sum()
    
    avg_roi = (total_revenue / total_spend - 1) * 100 if total_spend > 0 else 0
    avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
    avg_conversion_rate = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0
    avg_cac = total_spend / total_conversions if total_conversions > 0 else 0
    
    # Enhanced metrics display
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_campaigns = total_campaigns - 15 if total_campaigns > 15 else total_campaigns
        st.metric("Active Campaigns", total_campaigns, delta=delta_campaigns)
    with col2:
        st.metric("Total Spend", f"${total_spend:,.0f}", delta=f"${total_spend*0.1:,.0f}")
    with col3:
        st.metric("Total Revenue", f"${total_revenue:,.0f}", delta=f"${total_revenue*0.15:,.0f}")
    with col4:
        roi_delta = avg_roi - 50 if avg_roi > 50 else avg_roi
        st.metric("Average ROI", f"{avg_roi:.1f}%", delta=f"{roi_delta:.1f}%")
    with col5:
        st.metric("Conversions", f"{total_conversions:,.0f}", delta=f"{int(total_conversions*0.12):,}")
    
    # Performance indicators
    st.subheader("🎯 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ctr_status = "🟢 Excellent" if avg_ctr > 3 else "🟡 Good" if avg_ctr > 2 else "🔴 Needs Improvement"
        st.metric("Click-Through Rate", f"{avg_ctr:.2f}%", help=f"Status: {ctr_status}")
    with col2:
        conv_status = "🟢 Excellent" if avg_conversion_rate > 4 else "🟡 Good" if avg_conversion_rate > 2 else "🔴 Needs Improvement"
        st.metric("Conversion Rate", f"{avg_conversion_rate:.2f}%", help=f"Status: {conv_status}")
    with col3:
        cac_benchmark = 50  # Industry benchmark
        cac_status = "🟢 Efficient" if avg_cac < cac_benchmark else "🟡 Moderate" if avg_cac < cac_benchmark*1.5 else "🔴 High"
        st.metric("Avg. CAC", f"${avg_cac:.2f}", help=f"Status: {cac_status}")
    with col4:
        ltv_cac_ratio = 150 / avg_cac if avg_cac > 0 else 0  # Assuming avg LTV of $150
        ratio_status = "🟢 Healthy" if ltv_cac_ratio > 3 else "🟡 Moderate" if ltv_cac_ratio > 1 else "🔴 Poor"
        st.metric("LTV:CAC Ratio", f"{ltv_cac_ratio:.1f}:1", help=f"Status: {ratio_status}")
    
    # Campaign performance overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Campaign performance chart
        fig = visualizer.create_campaign_performance_chart(campaign_data['campaigns'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer segment distribution
        fig = visualizer.create_segment_distribution_chart(campaign_data['customers'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent performance trends
    st.subheader("📈 Performance Trends")
    performance_metrics = performance_tracker.calculate_performance_metrics(campaign_data)
    
    col1, col2 = st.columns(2)
    with col1:
        # ROI trend
        fig = visualizer.create_roi_trend_chart(campaign_data['daily_metrics'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Conversion rate trend
        fig = visualizer.create_conversion_trend_chart(campaign_data['daily_metrics'])
        st.plotly_chart(fig, use_container_width=True)

def display_campaign_analysis(campaign_data, campaign_analyzer, visualizer):
    """Display campaign analysis results"""
    st.header("🎯 AI Campaign Analysis")
    
    # Add analysis controls
    col1, col2 = st.columns(2)
    with col1:
        analysis_depth = st.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"])
    with col2:
        focus_area = st.selectbox("Focus Area", ["All Campaigns", "Underperforming", "Top Performers", "New Campaigns"])
    
    # Run campaign analysis
    with st.spinner(f"Running {analysis_depth.lower()} AI analysis on {focus_area.lower()}..."):
        analysis_results = campaign_analyzer.analyze_campaigns(campaign_data)
        
    # Performance Summary Cards
    st.subheader("📈 Performance Summary")
    summary = analysis_results['performance_summary']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(f"**Profitable Campaigns**\n{summary['campaigns_profitable']}/{summary['total_campaigns']}")
    with col2:
        best_channel = summary['best_performing_channel']
        st.success(f"**Top Channel**\n{best_channel.title()}")
    with col3:
        st.warning(f"**Needs Attention**\n{summary['campaigns_unprofitable']} campaigns")
    with col4:
        st.metric("Avg Conversion Rate", f"{summary['avg_conversion_rate']:.2f}%")
    
    # Display analysis results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performing Campaigns")
        top_campaigns = analysis_results['top_campaigns']
        for i, (idx, campaign) in enumerate(top_campaigns.iterrows()):
            with st.expander(f"#{i+1} {campaign['campaign_name']}"):
                st.metric("ROI", f"{campaign['roi']:.1f}%")
                st.metric("Conversion Rate", f"{campaign['conversion_rate']:.2f}%")
                st.metric("Revenue", f"${campaign['revenue']:,.0f}")
    
    with col2:
        st.subheader("⚠️ Underperforming Campaigns")
        underperforming = analysis_results['underperforming_campaigns']
        for i, (idx, campaign) in enumerate(underperforming.iterrows()):
            with st.expander(f"⚠️ {campaign['campaign_name']}"):
                st.metric("ROI", f"{campaign['roi']:.1f}%", delta=f"{campaign['roi']:.1f}%")
                st.metric("Conversion Rate", f"{campaign['conversion_rate']:.2f}%")
                st.write("**Recommendation:** ", analysis_results['recommendations'].get(campaign['campaign_name'], "Optimize targeting and creative"))
    
    # Customer segmentation analysis
    st.subheader("👥 Customer Segmentation Analysis")
    segmentation_results = campaign_analyzer.perform_customer_segmentation(campaign_data['customers'])
    
    col1, col2 = st.columns(2)
    with col1:
        fig = visualizer.create_segment_analysis_chart(segmentation_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Segment Insights")
        for segment, data in segmentation_results['segment_profiles'].items():
            with st.expander(f"Segment {segment}"):
                st.write(f"**Size:** {data['size']} customers")
                st.write(f"**Avg LTV:** ${data['avg_ltv']:.0f}")
                st.write(f"**Avg Age:** {data['avg_age']:.0f}")
                st.write(f"**Top Channel:** {data['preferred_channel']}")

def display_budget_optimization(campaign_data, budget_optimizer, visualizer):
    """Display budget optimization recommendations"""
    st.header("💰 AI Budget Optimization")
    
    # Advanced budget optimization controls
    col1, col2, col3 = st.columns(3)
    with col1:
        total_budget = st.number_input("Total Marketing Budget ($)", 
                                     min_value=10000, 
                                     max_value=1000000, 
                                     value=100000,
                                     step=5000)
    with col2:
        optimization_goal = st.selectbox("Optimization Goal", 
                                       ["ROI", "Revenue", "Conversions", "Reach"])
    with col3:
        time_horizon = st.selectbox("Time Horizon", 
                                  ["1 Month", "3 Months", "6 Months", "1 Year"])
    
    # Risk and constraint settings
    with st.expander("⚙️ Advanced Optimization Settings"):
        col1, col2 = st.columns(2)
        with col1:
            risk_tolerance = st.slider("Risk Tolerance", 0.1, 1.0, 0.5, 
                                     help="Higher values allow more aggressive budget shifts")
            min_budget_per_campaign = st.slider("Min Budget per Campaign (%)", 1, 20, 5)
        with col2:
            max_budget_per_campaign = st.slider("Max Budget per Campaign (%)", 30, 80, 40)
            diversification_factor = st.slider("Channel Diversification", 0.1, 1.0, 0.7,
                                             help="Higher values promote budget distribution across channels")
    
    if st.button("🎯 Optimize Budget Allocation", type="primary"):
        with st.spinner("Running budget optimization algorithms..."):
            optimization_results = budget_optimizer.optimize_budget_allocation(
                campaign_data, total_budget, optimization_goal.lower()
            )
        
        # Display optimization results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💡 Optimized Allocation")
            optimal_allocation = optimization_results['optimal_allocation']
            
            # Create allocation chart
            fig = visualizer.create_budget_allocation_chart(optimal_allocation)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Expected Results")
            expected_results = optimization_results['expected_results']
            
            st.metric("Expected ROI", f"{expected_results['roi']:.1f}%")
            st.metric("Expected Revenue", f"${expected_results['revenue']:,.0f}")
            st.metric("Expected Conversions", f"{expected_results['conversions']:,.0f}")
            
            # Budget recommendations
            st.subheader("🎯 Recommendations")
            recommendations = optimization_results['recommendations']
            for rec in recommendations:
                st.info(rec)
        
        # Detailed allocation table
        st.subheader("📋 Detailed Budget Allocation")
        allocation_df = pd.DataFrame(optimal_allocation)
        st.dataframe(allocation_df, use_container_width=True)

def display_performance_tracking(campaign_data, performance_tracker, visualizer):
    """Display performance tracking and analytics"""
    st.header("📈 Performance Tracking & Analytics")
    
    # Performance metrics calculation
    performance_metrics = performance_tracker.calculate_performance_metrics(campaign_data)
    
    # Key performance indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall CTR", f"{performance_metrics['overall_ctr']:.2f}%")
    with col2:
        st.metric("Avg Conversion Rate", f"{performance_metrics['avg_conversion_rate']:.2f}%")
    with col3:
        st.metric("Customer Acquisition Cost", f"${performance_metrics['avg_cac']:.2f}")
    with col4:
        st.metric("Lifetime Value", f"${performance_metrics['avg_ltv']:.2f}")
    
    # Performance tracking charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Campaign performance heatmap
        st.subheader("🔥 Campaign Performance Heatmap")
        fig = visualizer.create_performance_heatmap(campaign_data['campaigns'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Channel performance comparison
        st.subheader("📺 Channel Performance")
        fig = visualizer.create_channel_performance_chart(campaign_data['campaigns'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Predictive analytics
    st.subheader("🔮 Predictive Analytics")
    predictions = performance_tracker.predict_future_performance(campaign_data)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = visualizer.create_prediction_chart(predictions['revenue_forecast'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Performance Insights")
        insights = performance_tracker.generate_insights(campaign_data)
        for insight in insights:
            st.info(insight)

def display_ab_testing(campaign_data, ab_test_agent, visualizer):
    """Display A/B testing recommendations and results"""
    st.header("🧪 A/B Testing & Experimentation")
    
    # A/B testing dashboard controls
    col1, col2, col3 = st.columns(3)
    with col1:
        test_type_filter = st.selectbox("Test Type", ["All", "Landing Page", "Ad Creative", "Email", "CTA"])
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Planned", "Running", "Completed"])
    
    # Statistical significance settings
    with st.expander("📊 Statistical Settings"):
        col1, col2 = st.columns(2)
        with col1:
            confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
            minimum_effect = st.slider("Minimum Detectable Effect (%)", 1, 50, 10)
        with col2:
            power = st.slider("Statistical Power (%)", 70, 95, 80)
            test_duration_limit = st.slider("Max Test Duration (days)", 7, 60, 28)
    
    # A/B test suggestions with enhanced filtering
    test_suggestions = ab_test_agent.suggest_ab_tests(campaign_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Recommended A/B Tests")
        for i, suggestion in enumerate(test_suggestions['suggestions']):
            with st.expander(f"Test #{i+1}: {suggestion['test_name']}"):
                st.write(f"**Hypothesis:** {suggestion['hypothesis']}")
                st.write(f"**Variable:** {suggestion['variable']}")
                st.write(f"**Expected Impact:** {suggestion['expected_impact']}")
                st.write(f"**Duration:** {suggestion['duration']} days")
                st.write(f"**Sample Size:** {suggestion['sample_size']} users")
    
    with col2:
        st.subheader("📊 Test Results Analysis")
        # Simulate some A/B test results
        test_results = ab_test_agent.analyze_test_results(campaign_data)
        
        for test_name, results in test_results.items():
            with st.expander(f"📈 {test_name}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Control (A)", 
                            f"{results['control_rate']:.2f}%",
                            delta=None)
                with col_b:
                    st.metric("Variant (B)", 
                            f"{results['variant_rate']:.2f}%",
                            delta=f"{results['lift']:.1f}%")
                
                if results['significant']:
                    st.success(f"✅ Statistically significant (p={results['p_value']:.3f})")
                else:
                    st.warning(f"⚠️ Not statistically significant (p={results['p_value']:.3f})")
    
    # Test planning tool
    st.subheader("🎯 Test Planning Tool")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        test_type = st.selectbox("Test Type", ["Landing Page", "Ad Creative", "Email Subject", "CTA Button"])
    with col2:
        confidence_level = st.slider("Confidence Level", 80, 99, 95)
    with col3:
        minimum_effect = st.slider("Minimum Detectable Effect (%)", 1, 20, 5)
    
    if st.button("📊 Calculate Sample Size"):
        sample_size = ab_test_agent.calculate_sample_size(
            confidence_level=confidence_level/100,
            minimum_effect=minimum_effect/100
        )
        st.info(f"**Recommended Sample Size:** {sample_size:,} users per variant")
        st.info(f"**Total Test Duration:** {sample_size // 1000} days (assuming 1,000 daily visitors)")

def display_real_time_monitoring(campaign_data, real_time_monitor, visualizer):
    """Display real-time monitoring and alerts"""
    st.header("🚨 Real-Time Campaign Monitoring")
    
    # Real-time monitoring controls
    col1, col2, col3 = st.columns(3)
    with col1:
        auto_refresh_monitoring = st.checkbox("Auto-refresh Monitoring", value=True)
    with col2:
        alert_sensitivity = st.selectbox("Alert Sensitivity", ["Low", "Medium", "High"], index=1)
    with col3:
        notification_method = st.selectbox("Notifications", ["Dashboard", "Email", "Slack", "All"])
    
    # Get monitoring results
    monitoring_results = real_time_monitor.monitor_campaigns(campaign_data)
    alerts = monitoring_results['alerts']
    alert_summary = monitoring_results['alert_summary']
    health_score = monitoring_results['health_score']
    
    # System health overview
    st.subheader("🏥 System Health Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        health_color = "🟢" if health_score > 80 else "🟡" if health_score > 60 else "🔴"
        st.metric("System Health", f"{health_color} {health_score:.0f}/100")
    with col2:
        alert_color = "🔴" if alert_summary['critical_alerts'] > 0 else "🟡" if alert_summary['warning_alerts'] > 0 else "🟢"
        st.metric("Active Alerts", f"{alert_color} {alert_summary['total_alerts']}")
    with col3:
        st.metric("Critical Issues", alert_summary['critical_alerts'], 
                 delta=-alert_summary['critical_alerts'] if alert_summary['critical_alerts'] == 0 else None)
    with col4:
        campaigns_at_risk = sum(1 for alert in alerts if alert['type'] == 'critical')
        st.metric("Campaigns at Risk", campaigns_at_risk)
    
    # Alert dashboard
    if alerts:
        st.subheader("⚠️ Active Alerts")
        
        # Filter alerts by type
        alert_filter = st.selectbox("Filter by Alert Type", ["All", "Critical", "Warning", "Info"])
        
        filtered_alerts = alerts
        if alert_filter != "All":
            filtered_alerts = [alert for alert in alerts if alert['type'].lower() == alert_filter.lower()]
        
        # Display alerts
        for alert in filtered_alerts:
            alert_type = alert['type']
            if alert_type == 'critical':
                st.error(f"🚨 **{alert['category']}**: {alert['message']} - *{alert['campaign']}*")
            elif alert_type == 'warning':
                st.warning(f"⚠️ **{alert['category']}**: {alert['message']} - *{alert['campaign']}*")
            else:
                st.info(f"ℹ️ **{alert['category']}**: {alert['message']} - *{alert['campaign']}*")
    else:
        st.success("🎉 No active alerts! All campaigns are performing within normal parameters.")
    
    # Recommendations
    st.subheader("💡 AI Recommendations")
    recommendations = monitoring_results['recommendations']
    
    if recommendations:
        for rec in recommendations:
            priority_color = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            
            with st.expander(f"{priority_color} {rec['action']} - {rec['priority'].title()} Priority"):
                st.write(f"**Description:** {rec['description']}")
                st.write("**Suggested Steps:**")
                for step in rec['suggested_steps']:
                    st.write(f"• {step}")
    else:
        st.info("No specific recommendations at this time. System is operating optimally.")
    
    # Performance trends and anomaly detection
    st.subheader("📈 Performance Trends & Anomaly Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Campaign performance trend
        campaigns_df = campaign_data['campaigns']
        fig_trend = visualizer.create_campaign_performance_chart(campaigns_df)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Channel health heatmap
        fig_heatmap = visualizer.create_performance_heatmap(campaigns_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Alert configuration
    with st.expander("⚙️ Alert Configuration"):
        st.subheader("Customize Alert Thresholds")
        
        col1, col2 = st.columns(2)
        with col1:
            roi_critical = st.slider("ROI Critical Threshold (%)", -50, 0, -10)
            roi_warning = st.slider("ROI Warning Threshold (%)", 0, 50, 20)
            conversion_low = st.slider("Low Conversion Rate (%)", 0.1, 5.0, 1.0)
        
        with col2:
            cpc_high = st.slider("High CPC Threshold ($)", 1, 20, 10)
            budget_burn = st.slider("Budget Burn Rate (%)", 50, 95, 80)
            
        if st.button("Update Alert Thresholds"):
            new_thresholds = {
                'roi_critical': roi_critical,
                'roi_warning': roi_warning,
                'conversion_rate_low': conversion_low,
                'cpc_high': cpc_high,
                'budget_burn_rate': budget_burn / 100
            }
            real_time_monitor.update_alert_thresholds(new_thresholds)
            st.success("Alert thresholds updated successfully!")
    
    # Auto-refresh functionality for monitoring
    if auto_refresh_monitoring:
        st.markdown("🔄 **Auto-refresh enabled** - Monitoring data updates every 30 seconds")
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()
