import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class CampaignAnalyzer:
    """AI Agent for analyzing campaign performance and providing insights"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.performance_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.customer_segmentation_model = KMeans(n_clusters=4, random_state=42)
    
    def analyze_campaigns(self, campaign_data):
        """Perform comprehensive campaign analysis"""
        campaigns_df = campaign_data['campaigns']
        
        # Calculate performance metrics
        campaigns_df['roi'] = (campaigns_df['revenue'] / campaigns_df['budget_spent'] - 1) * 100
        campaigns_df['conversion_rate'] = (campaigns_df['conversions'] / campaigns_df['impressions']) * 100
        campaigns_df['cpc'] = campaigns_df['budget_spent'] / campaigns_df['clicks']
        campaigns_df['cpa'] = campaigns_df['budget_spent'] / campaigns_df['conversions']
        
        # Identify top performing campaigns
        top_campaigns = campaigns_df.nlargest(5, 'roi')
        
        # Identify underperforming campaigns
        underperforming_campaigns = campaigns_df[campaigns_df['roi'] < 0].nsmallest(5, 'roi')
        
        # Generate recommendations
        recommendations = self._generate_recommendations(campaigns_df)
        
        # Predict campaign success factors
        success_factors = self._analyze_success_factors(campaigns_df)
        
        return {
            'top_campaigns': top_campaigns,
            'underperforming_campaigns': underperforming_campaigns,
            'recommendations': recommendations,
            'success_factors': success_factors,
            'performance_summary': self._create_performance_summary(campaigns_df)
        }
    
    def perform_customer_segmentation(self, customers_df):
        """Perform customer segmentation analysis"""
        # Prepare features for clustering
        features = ['age', 'income', 'lifetime_value', 'engagement_score']
        X = customers_df[features].fillna(0)
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform clustering
        clusters = self.customer_segmentation_model.fit_predict(X_scaled)
        customers_df['segment'] = clusters
        
        # Analyze segment characteristics
        segment_profiles = {}
        for segment in range(4):
            segment_data = customers_df[customers_df['segment'] == segment]
            segment_profiles[segment] = {
                'size': len(segment_data),
                'avg_age': segment_data['age'].mean(),
                'avg_income': segment_data['income'].mean(),
                'avg_ltv': segment_data['lifetime_value'].mean(),
                'avg_engagement': segment_data['engagement_score'].mean(),
                'preferred_channel': segment_data['preferred_channel'].mode().iloc[0] if not segment_data['preferred_channel'].mode().empty else 'Unknown'
            }
        
        return {
            'segmented_customers': customers_df,
            'segment_profiles': segment_profiles,
            'cluster_centers': self.customer_segmentation_model.cluster_centers_
        }
    
    def _generate_recommendations(self, campaigns_df):
        """Generate AI-powered recommendations for campaigns"""
        recommendations = {}
        
        for idx, campaign in campaigns_df.iterrows():
            campaign_recs = []
            
            # ROI-based recommendations
            if campaign['roi'] < 0:
                campaign_recs.append("Consider pausing this campaign and reallocating budget")
            elif campaign['roi'] < 50:
                campaign_recs.append("Optimize targeting parameters to improve ROI")
            
            # Conversion rate recommendations
            if campaign['conversion_rate'] < 2:
                campaign_recs.append("Improve landing page design and call-to-action")
            
            # Cost efficiency recommendations
            if campaign['cpc'] > campaigns_df['cpc'].median() * 1.5:
                campaign_recs.append("Optimize bidding strategy to reduce cost per click")
            
            # Channel-specific recommendations
            if campaign['channel'] == 'social_media' and campaign['engagement_rate'] < 3:
                campaign_recs.append("Create more engaging social media content")
            elif campaign['channel'] == 'search' and campaign['click_through_rate'] < 2:
                campaign_recs.append("Improve ad copy and keyword relevance")
            
            recommendations[campaign['campaign_name']] = "; ".join(campaign_recs) if campaign_recs else "Campaign performing well"
        
        return recommendations
    
    def _analyze_success_factors(self, campaigns_df):
        """Analyze factors that contribute to campaign success"""
        # Prepare features for analysis
        feature_columns = ['budget_spent', 'impressions', 'clicks', 'click_through_rate', 'engagement_rate']
        X = campaigns_df[feature_columns].fillna(0)
        y = campaigns_df['roi']
        
        # Train model to understand success factors
        self.performance_model.fit(X, y)
        
        # Get feature importance
        feature_importance = dict(zip(feature_columns, self.performance_model.feature_importances_))
        
        # Sort by importance
        sorted_factors = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'most_important_factors': sorted_factors[:3],
            'feature_importance': feature_importance,
            'model_score': self.performance_model.score(X, y)
        }
    
    def _create_performance_summary(self, campaigns_df):
        """Create a comprehensive performance summary"""
        summary = {
            'total_campaigns': len(campaigns_df),
            'avg_roi': campaigns_df['roi'].mean(),
            'avg_conversion_rate': campaigns_df['conversion_rate'].mean(),
            'total_spend': campaigns_df['budget_spent'].sum(),
            'total_revenue': campaigns_df['revenue'].sum(),
            'best_performing_channel': campaigns_df.groupby('channel')['roi'].mean().idxmax(),
            'worst_performing_channel': campaigns_df.groupby('channel')['roi'].mean().idxmin(),
            'campaigns_profitable': len(campaigns_df[campaigns_df['roi'] > 0]),
            'campaigns_unprofitable': len(campaigns_df[campaigns_df['roi'] < 0])
        }
        
        return summary
    
    def predict_campaign_performance(self, campaign_features):
        """Predict expected performance for new campaign parameters"""
        if hasattr(self.performance_model, 'predict'):
            prediction = self.performance_model.predict([campaign_features])
            return prediction[0]
        return 0
    
    def get_optimization_insights(self, campaigns_df):
        """Get insights for campaign optimization"""
        insights = []
        
        # Budget allocation insights
        channel_performance = campaigns_df.groupby('channel').agg({
            'roi': 'mean',
            'budget_spent': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        best_channel = channel_performance.loc[channel_performance['roi'].idxmax(), 'channel']
        insights.append(f"Channel '{best_channel}' shows highest ROI - consider increasing budget allocation")
        
        # Timing insights
        if 'day_of_week' in campaigns_df.columns:
            day_performance = campaigns_df.groupby('day_of_week')['conversion_rate'].mean()
            best_day = day_performance.idxmax()
            insights.append(f"Campaigns perform best on {best_day} - optimize scheduling")
        
        # Creative insights
        if campaigns_df['engagement_rate'].std() > 1:
            insights.append("High variation in engagement rates - test different creative approaches")
        
        return insights
