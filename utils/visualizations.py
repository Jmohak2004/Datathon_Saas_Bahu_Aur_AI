import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class DashboardVisualizer:
    """Utility class for creating interactive visualizations"""
    
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
        self.theme = {
            'background_color': '#ffffff',
            'grid_color': '#f0f0f0',
            'text_color': '#333333'
        }
    
    def create_campaign_performance_chart(self, campaigns_df):
        """Create campaign performance scatter plot"""
        fig = px.scatter(
            campaigns_df,
            x='budget_spent',
            y='revenue',
            size='conversions',
            color='channel',
            hover_data=['campaign_name', 'roi', 'conversion_rate'],
            title='Campaign Performance: Budget vs Revenue',
            labels={
                'budget_spent': 'Budget Spent ($)',
                'revenue': 'Revenue ($)',
                'conversions': 'Conversions'
            }
        )
        
        # Add diagonal line for break-even
        max_val = max(campaigns_df['budget_spent'].max(), campaigns_df['revenue'].max())
        fig.add_shape(
            type="line",
            x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="red", width=2, dash="dash"),
            name="Break-even line"
        )
        
        fig.update_layout(
            height=500,
            showlegend=True,
            title_x=0.5
        )
        
        return fig
    
    def create_segment_distribution_chart(self, customers_df):
        """Create customer segment distribution pie chart"""
        if 'segment' not in customers_df.columns:
            # Create segments based on age if not available
            customers_df['segment'] = pd.cut(
                customers_df['age'], 
                bins=[0, 25, 40, 55, 100], 
                labels=['Gen Z', 'Millennials', 'Gen X', 'Boomers']
            )
        
        segment_counts = customers_df['segment'].value_counts()
        
        fig = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title='Customer Segment Distribution',
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_roi_trend_chart(self, daily_metrics):
        """Create ROI trend line chart"""
        fig = px.line(
            daily_metrics,
            x='date',
            y='roi',
            title='ROI Trend Over Time',
            labels={'roi': 'ROI (%)', 'date': 'Date'}
        )
        
        # Add moving average
        if len(daily_metrics) > 7:
            daily_metrics['roi_ma7'] = daily_metrics['roi'].rolling(window=7).mean()
            fig.add_scatter(
                x=daily_metrics['date'],
                y=daily_metrics['roi_ma7'],
                mode='lines',
                name='7-day Moving Average',
                line=dict(color='red', width=2)
            )
        
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_conversion_trend_chart(self, daily_metrics):
        """Create conversion rate trend chart"""
        fig = px.line(
            daily_metrics,
            x='date',
            y='conversion_rate',
            title='Conversion Rate Trend',
            labels={'conversion_rate': 'Conversion Rate (%)', 'date': 'Date'}
        )
        
        # Add average line
        avg_conversion = daily_metrics['conversion_rate'].mean()
        fig.add_hline(
            y=avg_conversion,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Average: {avg_conversion:.2f}%"
        )
        
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_segment_analysis_chart(self, segmentation_results):
        """Create customer segment analysis chart"""
        if 'segment_profiles' in segmentation_results:
            profiles = segmentation_results['segment_profiles']
            
            # Prepare data for visualization
            segments = []
            sizes = []
            avg_ltvs = []
            avg_ages = []
            
            for segment, data in profiles.items():
                segments.append(f"Segment {segment}")
                sizes.append(data['size'])
                avg_ltvs.append(data['avg_ltv'])
                avg_ages.append(data['avg_age'])
            
            # Create subplot
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Segment Sizes', 'Average LTV by Segment'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Segment sizes
            fig.add_trace(
                go.Bar(x=segments, y=sizes, name='Segment Size', marker_color='lightblue'),
                row=1, col=1
            )
            
            # Average LTV
            fig.add_trace(
                go.Bar(x=segments, y=avg_ltvs, name='Avg LTV', marker_color='lightgreen'),
                row=1, col=2
            )
            
            fig.update_layout(height=400, title_text="Customer Segment Analysis", title_x=0.5)
            
            return fig
        
        return go.Figure()
    
    def create_budget_allocation_chart(self, allocation_data):
        """Create budget allocation chart"""
        df = pd.DataFrame(allocation_data)
        
        fig = px.bar(
            df,
            x='campaign_name',
            y='optimal_budget',
            color='channel',
            title='Optimized Budget Allocation',
            labels={'optimal_budget': 'Optimal Budget ($)', 'campaign_name': 'Campaign'}
        )
        
        fig.update_xaxis(tickangle=45)
        fig.update_layout(height=500, title_x=0.5)
        
        return fig
    
    def create_performance_heatmap(self, campaigns_df):
        """Create campaign performance heatmap"""
        # Prepare data for heatmap
        metrics = ['roi', 'conversion_rate', 'click_through_rate', 'engagement_rate']
        
        # Normalize metrics to 0-100 scale for better visualization
        heatmap_data = campaigns_df[metrics].copy()
        for metric in metrics:
            heatmap_data[metric] = (heatmap_data[metric] - heatmap_data[metric].min()) / \
                                 (heatmap_data[metric].max() - heatmap_data[metric].min()) * 100
        
        fig = px.imshow(
            heatmap_data.T,
            aspect='auto',
            title='Campaign Performance Heatmap (Normalized)',
            labels={'x': 'Campaign Index', 'y': 'Metrics', 'color': 'Performance Score'}
        )
        
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_channel_performance_chart(self, campaigns_df):
        """Create channel performance comparison chart"""
        channel_metrics = campaigns_df.groupby('channel').agg({
            'roi': 'mean',
            'conversion_rate': 'mean',
            'click_through_rate': 'mean',
            'revenue': 'sum'
        }).reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average ROI', 'Average Conversion Rate', 'Average CTR', 'Total Revenue'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # ROI
        fig.add_trace(
            go.Bar(x=channel_metrics['channel'], y=channel_metrics['roi'], name='ROI'),
            row=1, col=1
        )
        
        # Conversion Rate
        fig.add_trace(
            go.Bar(x=channel_metrics['channel'], y=channel_metrics['conversion_rate'], name='Conv Rate'),
            row=1, col=2
        )
        
        # CTR
        fig.add_trace(
            go.Bar(x=channel_metrics['channel'], y=channel_metrics['click_through_rate'], name='CTR'),
            row=2, col=1
        )
        
        # Revenue
        fig.add_trace(
            go.Bar(x=channel_metrics['channel'], y=channel_metrics['revenue'], name='Revenue'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, title_text="Channel Performance Comparison", title_x=0.5)
        
        return fig
    
    def create_prediction_chart(self, forecast_data):
        """Create prediction/forecast chart"""
        if not forecast_data or 'dates' not in forecast_data:
            return go.Figure()
        
        fig = px.line(
            x=forecast_data['dates'],
            y=forecast_data['predictions'],
            title='Revenue Forecast',
            labels={'x': 'Date', 'y': 'Predicted Revenue ($)'}
        )
        
        # Add confidence interval if available
        if 'confidence_upper' in forecast_data and 'confidence_lower' in forecast_data:
            fig.add_trace(
                go.Scatter(
                    x=forecast_data['dates'],
                    y=forecast_data['confidence_upper'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(0,100,80,0)',
                    showlegend=False
                )
            )
            
            fig.add_trace(
                go.Scatter(
                    x=forecast_data['dates'],
                    y=forecast_data['confidence_lower'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(0,100,80,0)',
                    name='Confidence Interval'
                )
            )
        
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_ab_test_results_chart(self, test_results):
        """Create A/B test results visualization"""
        test_names = list(test_results.keys())
        control_rates = [test_results[name]['control_rate'] for name in test_names]
        variant_rates = [test_results[name]['variant_rate'] for name in test_names]
        significance = [test_results[name]['significant'] for name in test_names]
        
        fig = go.Figure()
        
        # Control rates
        fig.add_trace(go.Bar(
            name='Control (A)',
            x=test_names,
            y=control_rates,
            marker_color='lightblue'
        ))
        
        # Variant rates
        fig.add_trace(go.Bar(
            name='Variant (B)',
            x=test_names,
            y=variant_rates,
            marker_color='lightgreen'
        ))
        
        # Add significance markers
        for i, (name, sig) in enumerate(zip(test_names, significance)):
            if sig:
                fig.add_annotation(
                    x=i,
                    y=max(control_rates[i], variant_rates[i]) + 0.1,
                    text="✓ Significant",
                    showarrow=False,
                    font=dict(color="green", size=12)
                )
        
        fig.update_layout(
            title='A/B Test Results Comparison',
            xaxis_title='Test Name',
            yaxis_title='Conversion Rate (%)',
            barmode='group',
            height=500,
            title_x=0.5
        )
        
        return fig
    
    def create_funnel_chart(self, funnel_data):
        """Create marketing funnel visualization"""
        stages = ['Impressions', 'Clicks', 'Conversions', 'Revenue']
        values = [
            funnel_data.get('impressions', 100000),
            funnel_data.get('clicks', 3000),
            funnel_data.get('conversions', 150),
            funnel_data.get('revenue', 15000)
        ]
        
        # Normalize revenue to show as percentage of impressions
        if len(values) > 3:
            values[3] = values[3] / 100  # Scale down revenue for visualization
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(
            title="Marketing Funnel Analysis",
            height=400,
            title_x=0.5
        )
        
        return fig
    
    def create_cohort_analysis_chart(self, cohort_data):
        """Create customer cohort analysis chart"""
        # Simulate cohort data if not provided
        if not cohort_data:
            months = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6']
            cohorts = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024']
            
            # Generate sample retention rates
            retention_data = []
            for cohort in cohorts:
                retention_rates = [100]  # Start at 100%
                for i in range(1, len(months)):
                    retention_rates.append(retention_rates[-1] * np.random.uniform(0.8, 0.95))
                retention_data.append(retention_rates)
            
            cohort_data = pd.DataFrame(retention_data, columns=months, index=cohorts)
        
        fig = px.imshow(
            cohort_data,
            aspect='auto',
            title='Customer Retention Cohort Analysis',
            labels={'x': 'Period', 'y': 'Cohort', 'color': 'Retention Rate (%)'}
        )
        
        fig.update_layout(height=400, title_x=0.5)
        
        return fig
    
    def create_attribution_chart(self, attribution_data):
        """Create marketing attribution chart"""
        # Default attribution data if not provided
        if not attribution_data:
            attribution_data = {
                'channels': ['Search', 'Social', 'Email', 'Display', 'Direct'],
                'first_touch': [30, 25, 15, 20, 10],
                'last_touch': [35, 20, 20, 15, 10],
                'linear': [25, 22, 18, 20, 15]
            }
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='First Touch',
            x=attribution_data['channels'],
            y=attribution_data['first_touch']
        ))
        
        fig.add_trace(go.Bar(
            name='Last Touch',
            x=attribution_data['channels'],
            y=attribution_data['last_touch']
        ))
        
        fig.add_trace(go.Bar(
            name='Linear Attribution',
            x=attribution_data['channels'],
            y=attribution_data['linear']
        ))
        
        fig.update_layout(
            title='Marketing Attribution Model Comparison',
            xaxis_title='Channel',
            yaxis_title='Attribution (%)',
            barmode='group',
            height=400,
            title_x=0.5
        )
        
        return fig
