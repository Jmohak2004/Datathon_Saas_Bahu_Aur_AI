import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PerformanceTracker:
    """AI Agent for tracking and predicting campaign performance"""
    
    def __init__(self):
        self.revenue_model = LinearRegression()
        self.conversion_model = LinearRegression()
        self.trend_models = {}
        
    def calculate_performance_metrics(self, campaign_data):
        """Calculate comprehensive performance metrics"""
        campaigns_df = campaign_data['campaigns']
        customers_df = campaign_data['customers']
        
        # Basic performance metrics
        total_impressions = campaigns_df['impressions'].sum()
        total_clicks = campaigns_df['clicks'].sum()
        total_conversions = campaigns_df['conversions'].sum()
        total_spend = campaigns_df['budget_spent'].sum()
        total_revenue = campaigns_df['revenue'].sum()
        
        # Calculate derived metrics
        overall_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
        avg_conversion_rate = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0
        avg_cac = total_spend / total_conversions if total_conversions > 0 else 0
        avg_ltv = customers_df['lifetime_value'].mean()
        overall_roi = ((total_revenue / total_spend) - 1) * 100 if total_spend > 0 else 0
        
        # Channel-specific metrics
        channel_metrics = campaigns_df.groupby('channel').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'conversions': 'sum',
            'budget_spent': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        channel_metrics['ctr'] = (channel_metrics['clicks'] / channel_metrics['impressions']) * 100
        channel_metrics['conversion_rate'] = (channel_metrics['conversions'] / channel_metrics['clicks']) * 100
        channel_metrics['roi'] = ((channel_metrics['revenue'] / channel_metrics['budget_spent']) - 1) * 100
        
        # Time-based performance trends
        if 'daily_metrics' in campaign_data:
            daily_trends = self._calculate_daily_trends(campaign_data['daily_metrics'])
        else:
            daily_trends = {}
        
        return {
            'overall_ctr': overall_ctr,
            'avg_conversion_rate': avg_conversion_rate,
            'avg_cac': avg_cac,
            'avg_ltv': avg_ltv,
            'overall_roi': overall_roi,
            'ltv_cac_ratio': avg_ltv / avg_cac if avg_cac > 0 else 0,
            'channel_metrics': channel_metrics,
            'daily_trends': daily_trends,
            'total_campaigns': len(campaigns_df),
            'active_customers': len(customers_df)
        }
    
    def predict_future_performance(self, campaign_data, forecast_days=30):
        """Predict future campaign performance"""
        campaigns_df = campaign_data['campaigns']
        
        # Prepare historical data for prediction
        if 'daily_metrics' in campaign_data:
            daily_data = campaign_data['daily_metrics'].copy()
        else:
            # Create synthetic daily data from campaign data
            daily_data = self._create_daily_data_from_campaigns(campaigns_df, forecast_days)
        
        # Train prediction models
        predictions = {}
        
        # Revenue prediction
        revenue_forecast = self._predict_revenue_trend(daily_data, forecast_days)
        predictions['revenue_forecast'] = revenue_forecast
        
        # Conversion prediction
        conversion_forecast = self._predict_conversion_trend(daily_data, forecast_days)
        predictions['conversion_forecast'] = conversion_forecast
        
        # ROI prediction
        roi_forecast = self._predict_roi_trend(daily_data, forecast_days)
        predictions['roi_forecast'] = roi_forecast
        
        # Campaign-specific predictions
        campaign_predictions = self._predict_individual_campaigns(campaigns_df, forecast_days)
        predictions['campaign_predictions'] = campaign_predictions
        
        return predictions
    
    def generate_insights(self, campaign_data):
        """Generate actionable insights from performance data"""
        campaigns_df = campaign_data['campaigns']
        metrics = self.calculate_performance_metrics(campaign_data)
        
        insights = []
        
        # ROI insights
        if metrics['overall_roi'] > 100:
            insights.append("🎉 Excellent overall ROI performance! Consider scaling successful campaigns.")
        elif metrics['overall_roi'] > 50:
            insights.append("✅ Good ROI performance with room for optimization.")
        elif metrics['overall_roi'] > 0:
            insights.append("⚠️ Positive but low ROI. Focus on campaign optimization.")
        else:
            insights.append("🚨 Negative ROI detected. Immediate campaign review required.")
        
        # Channel performance insights
        best_channel = metrics['channel_metrics'].loc[metrics['channel_metrics']['roi'].idxmax()]
        worst_channel = metrics['channel_metrics'].loc[metrics['channel_metrics']['roi'].idxmin()]
        
        insights.append(f"🏆 Best performing channel: {best_channel['channel']} (ROI: {best_channel['roi']:.1f}%)")
        insights.append(f"📉 Underperforming channel: {worst_channel['channel']} (ROI: {worst_channel['roi']:.1f}%)")
        
        # Conversion rate insights
        if metrics['avg_conversion_rate'] < 2:
            insights.append("🎯 Low conversion rates detected. Consider improving landing pages and targeting.")
        elif metrics['avg_conversion_rate'] > 5:
            insights.append("🔥 High conversion rates! Your targeting and creative are performing well.")
        
        # LTV:CAC ratio insights
        if metrics['ltv_cac_ratio'] > 3:
            insights.append("💰 Excellent LTV:CAC ratio. Strong customer value creation.")
        elif metrics['ltv_cac_ratio'] > 1:
            insights.append("📊 Positive LTV:CAC ratio. Consider optimizing for higher customer lifetime value.")
        else:
            insights.append("⚠️ Low LTV:CAC ratio. Focus on reducing acquisition costs or increasing customer value.")
        
        # Campaign distribution insights
        top_campaign = campaigns_df.loc[campaigns_df['revenue'].idxmax()]
        insights.append(f"🌟 Top revenue generator: {top_campaign['campaign_name']} (${top_campaign['revenue']:,.0f})")
        
        # Budget efficiency insights
        campaigns_df['efficiency'] = campaigns_df['revenue'] / campaigns_df['budget_spent']
        efficient_campaigns = campaigns_df[campaigns_df['efficiency'] > campaigns_df['efficiency'].median()]
        insights.append(f"⚡ {len(efficient_campaigns)} campaigns are above median efficiency")
        
        return insights
    
    def track_campaign_health(self, campaign_data):
        """Track overall campaign health and identify issues"""
        campaigns_df = campaign_data['campaigns']
        
        health_score = 0
        health_factors = []
        
        # ROI health (30% weight)
        avg_roi = ((campaigns_df['revenue'].sum() / campaigns_df['budget_spent'].sum()) - 1) * 100
        if avg_roi > 100:
            roi_score = 100
        elif avg_roi > 50:
            roi_score = 80
        elif avg_roi > 0:
            roi_score = 60
        else:
            roi_score = 20
        
        health_score += roi_score * 0.3
        health_factors.append(f"ROI Health: {roi_score}/100")
        
        # Conversion rate health (25% weight)
        avg_conv_rate = (campaigns_df['conversions'].sum() / campaigns_df['clicks'].sum()) * 100
        if avg_conv_rate > 5:
            conv_score = 100
        elif avg_conv_rate > 2:
            conv_score = 80
        elif avg_conv_rate > 1:
            conv_score = 60
        else:
            conv_score = 40
        
        health_score += conv_score * 0.25
        health_factors.append(f"Conversion Health: {conv_score}/100")
        
        # Campaign diversity health (20% weight)
        channel_count = campaigns_df['channel'].nunique()
        if channel_count >= 4:
            diversity_score = 100
        elif channel_count >= 3:
            diversity_score = 80
        elif channel_count >= 2:
            diversity_score = 60
        else:
            diversity_score = 40
        
        health_score += diversity_score * 0.2
        health_factors.append(f"Diversity Health: {diversity_score}/100")
        
        # Performance consistency health (25% weight)
        roi_std = campaigns_df['revenue'].std() / campaigns_df['revenue'].mean()
        if roi_std < 0.5:
            consistency_score = 100
        elif roi_std < 1:
            consistency_score = 80
        elif roi_std < 1.5:
            consistency_score = 60
        else:
            consistency_score = 40
        
        health_score += consistency_score * 0.25
        health_factors.append(f"Consistency Health: {consistency_score}/100")
        
        # Determine health status
        if health_score >= 90:
            health_status = "Excellent"
        elif health_score >= 75:
            health_status = "Good"
        elif health_score >= 60:
            health_status = "Fair"
        else:
            health_status = "Poor"
        
        return {
            'overall_health_score': round(health_score, 1),
            'health_status': health_status,
            'health_factors': health_factors,
            'recommendations': self._generate_health_recommendations(health_score, health_factors)
        }
    
    def _calculate_daily_trends(self, daily_metrics):
        """Calculate trends from daily metrics"""
        daily_metrics['date'] = pd.to_datetime(daily_metrics['date'])
        daily_metrics = daily_metrics.sort_values('date')
        
        # Calculate moving averages
        daily_metrics['revenue_ma7'] = daily_metrics['revenue'].rolling(window=7).mean()
        daily_metrics['conversion_rate_ma7'] = daily_metrics['conversion_rate'].rolling(window=7).mean()
        daily_metrics['roi_ma7'] = daily_metrics['roi'].rolling(window=7).mean()
        
        return daily_metrics
    
    def _create_daily_data_from_campaigns(self, campaigns_df, days):
        """Create synthetic daily data from campaign data"""
        start_date = datetime.now() - timedelta(days=days)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        daily_data = []
        for date in dates:
            # Simulate daily performance with some randomness
            daily_revenue = campaigns_df['revenue'].sum() / days * np.random.normal(1, 0.2)
            daily_conversions = campaigns_df['conversions'].sum() / days * np.random.normal(1, 0.15)
            daily_spend = campaigns_df['budget_spent'].sum() / days * np.random.normal(1, 0.1)
            
            daily_data.append({
                'date': date,
                'revenue': max(daily_revenue, 0),
                'conversions': max(daily_conversions, 0),
                'spend': max(daily_spend, 0),
                'conversion_rate': np.random.normal(2.5, 0.5),
                'roi': ((daily_revenue / daily_spend - 1) * 100) if daily_spend > 0 else 0
            })
        
        return pd.DataFrame(daily_data)
    
    def _predict_revenue_trend(self, daily_data, forecast_days):
        """Predict revenue trend"""
        if len(daily_data) < 7:
            return {}
        
        # Prepare data for prediction
        daily_data['day_num'] = range(len(daily_data))
        X = daily_data[['day_num']].values
        y = daily_data['revenue'].values
        
        # Train model
        self.revenue_model.fit(X, y)
        
        # Make predictions
        future_days = range(len(daily_data), len(daily_data) + forecast_days)
        future_X = np.array(future_days).reshape(-1, 1)
        predictions = self.revenue_model.predict(future_X)
        
        # Create forecast data
        forecast_dates = [daily_data['date'].max() + timedelta(days=i+1) for i in range(forecast_days)]
        
        return {
            'dates': forecast_dates,
            'predictions': predictions.tolist(),
            'model_score': self.revenue_model.score(X, y),
            'trend': 'increasing' if predictions[-1] > predictions[0] else 'decreasing'
        }
    
    def _predict_conversion_trend(self, daily_data, forecast_days):
        """Predict conversion trend"""
        if len(daily_data) < 7:
            return {}
        
        daily_data['day_num'] = range(len(daily_data))
        X = daily_data[['day_num']].values
        y = daily_data['conversion_rate'].values
        
        self.conversion_model.fit(X, y)
        
        future_days = range(len(daily_data), len(daily_data) + forecast_days)
        future_X = np.array(future_days).reshape(-1, 1)
        predictions = self.conversion_model.predict(future_X)
        
        forecast_dates = [daily_data['date'].max() + timedelta(days=i+1) for i in range(forecast_days)]
        
        return {
            'dates': forecast_dates,
            'predictions': predictions.tolist(),
            'model_score': self.conversion_model.score(X, y)
        }
    
    def _predict_roi_trend(self, daily_data, forecast_days):
        """Predict ROI trend"""
        # Simple trend analysis for ROI
        recent_roi = daily_data['roi'].tail(7).mean()
        historical_roi = daily_data['roi'].head(7).mean()
        
        trend_direction = 1 if recent_roi > historical_roi else -1
        trend_strength = abs(recent_roi - historical_roi) / historical_roi if historical_roi != 0 else 0
        
        # Generate predictions with trend
        predictions = []
        base_roi = recent_roi
        
        for i in range(forecast_days):
            predicted_roi = base_roi + (trend_direction * trend_strength * i * 0.1)
            predictions.append(predicted_roi)
        
        forecast_dates = [daily_data['date'].max() + timedelta(days=i+1) for i in range(forecast_days)]
        
        return {
            'dates': forecast_dates,
            'predictions': predictions,
            'trend_direction': 'positive' if trend_direction > 0 else 'negative'
        }
    
    def _predict_individual_campaigns(self, campaigns_df, forecast_days):
        """Predict individual campaign performance"""
        predictions = {}
        
        for idx, campaign in campaigns_df.iterrows():
            # Simple prediction based on current performance
            daily_revenue = campaign['revenue'] / 30  # Assume 30-day campaign
            daily_conversions = campaign['conversions'] / 30
            
            # Add some trend and randomness
            trend_factor = np.random.normal(1, 0.1)
            
            predicted_revenue = [daily_revenue * trend_factor * (1 + i * 0.01) for i in range(forecast_days)]
            predicted_conversions = [daily_conversions * trend_factor * (1 + i * 0.01) for i in range(forecast_days)]
            
            predictions[campaign['campaign_name']] = {
                'revenue_forecast': predicted_revenue,
                'conversion_forecast': predicted_conversions,
                'confidence': 0.75  # Mock confidence score
            }
        
        return predictions
    
    def _generate_health_recommendations(self, health_score, health_factors):
        """Generate recommendations based on health score"""
        recommendations = []
        
        if health_score < 60:
            recommendations.append("🚨 Urgent: Comprehensive campaign review needed")
            recommendations.append("🎯 Focus on improving conversion rates and ROI")
            recommendations.append("📊 Consider A/B testing different approaches")
        elif health_score < 75:
            recommendations.append("⚠️ Optimize underperforming campaigns")
            recommendations.append("🔄 Reallocate budget to high-performing channels")
        else:
            recommendations.append("✅ Maintain current strategy while exploring scaling opportunities")
            recommendations.append("🚀 Consider expanding to new channels or audiences")
        
        return recommendations
