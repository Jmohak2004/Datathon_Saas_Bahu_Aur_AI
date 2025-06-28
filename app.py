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
from utils.data_generator import DataGenerator
from utils.visualizations import DashboardVisualizer

# Configure page
st.set_page_config(
    page_title="AI Marketing Campaign Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    visualizer = DashboardVisualizer()
    
    return data_gen, campaign_analyzer, budget_optimizer, performance_tracker, ab_test_agent, visualizer

def main():
    # Header
    st.title("🚀 AI-Powered Marketing Campaign Optimizer")
    st.markdown("**Multi-Agent System for Digital Marketing Excellence**")
    
    # Initialize system components
    data_gen, campaign_analyzer, budget_optimizer, performance_tracker, ab_test_agent, visualizer = initialize_system()
    
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
        if auto_refresh:
            refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 10)
    
    # Main content area
    if not st.session_state.data_generated:
        st.info("👈 Please generate campaign data using the sidebar controls to begin analysis.")
        return
    
    # Get campaign data
    campaign_data = st.session_state.campaign_data
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard Overview", 
        "🎯 Campaign Analysis", 
        "💰 Budget Optimization", 
        "📈 Performance Tracking", 
        "🧪 A/B Testing"
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
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

def display_dashboard_overview(campaign_data, visualizer, performance_tracker):
    """Display the main dashboard overview"""
    st.header("📊 Campaign Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_campaigns = len(campaign_data['campaigns'])
    total_spend = campaign_data['campaigns']['budget_spent'].sum()
    total_revenue = campaign_data['campaigns']['revenue'].sum()
    avg_roi = (total_revenue / total_spend - 1) * 100 if total_spend > 0 else 0
    
    with col1:
        st.metric("Total Campaigns", total_campaigns)
    with col2:
        st.metric("Total Spend", f"${total_spend:,.0f}")
    with col3:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    with col4:
        st.metric("Average ROI", f"{avg_roi:.1f}%")
    
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
    
    # Run campaign analysis
    with st.spinner("Analyzing campaigns with AI..."):
        analysis_results = campaign_analyzer.analyze_campaigns(campaign_data)
    
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
    
    # Budget optimization controls
    col1, col2 = st.columns(2)
    with col1:
        total_budget = st.number_input("Total Marketing Budget ($)", 
                                     min_value=10000, 
                                     max_value=1000000, 
                                     value=100000,
                                     step=5000)
    with col2:
        optimization_goal = st.selectbox("Optimization Goal", 
                                       ["ROI", "Revenue", "Conversions", "Reach"])
    
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
    
    # A/B test suggestions
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

if __name__ == "__main__":
    main()
