import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataGenerator:
    """Utility class for generating realistic marketing campaign data"""
    
    def __init__(self):
        self.channels = ['search', 'social_media', 'display', 'email', 'video']
        self.campaign_types = ['awareness', 'conversion', 'retargeting', 'lead_gen']
        self.customer_segments = ['millennials', 'gen_x', 'gen_z', 'baby_boomers']
        
    def generate_campaign_data(self, num_campaigns=20, num_customers=5000, date_range=30):
        """Generate comprehensive campaign data"""
        # Generate campaigns
        campaigns = self._generate_campaigns(num_campaigns, date_range)
        
        # Generate customers
        customers = self._generate_customers(num_customers)
        
        # Generate daily metrics
        daily_metrics = self._generate_daily_metrics(date_range)
        
        # Generate customer interactions
        interactions = self._generate_customer_interactions(campaigns, customers, num_interactions=num_campaigns*50)
        
        return {
            'campaigns': campaigns,
            'customers': customers,
            'daily_metrics': daily_metrics,
            'interactions': interactions
        }
    
    def _generate_campaigns(self, num_campaigns, date_range):
        """Generate realistic campaign data"""
        campaigns = []
        
        for i in range(num_campaigns):
            # Base metrics
            budget_allocated = random.randint(5000, 50000)
            budget_spent = budget_allocated * random.uniform(0.7, 1.0)
            
            # Channel-specific performance variations
            channel = random.choice(self.channels)
            channel_multipliers = {
                'search': {'ctr': 1.2, 'conversion': 1.3, 'cpc': 1.1},
                'social_media': {'ctr': 0.8, 'conversion': 0.9, 'cpc': 0.7},
                'display': {'ctr': 0.6, 'conversion': 0.7, 'cpc': 0.5},
                'email': {'ctr': 1.5, 'conversion': 1.4, 'cpc': 0.3},
                'video': {'ctr': 1.0, 'conversion': 1.1, 'cpc': 1.2}
            }
            
            multiplier = channel_multipliers[channel]
            
            # Calculate traffic metrics
            cpc = random.uniform(1, 5) * multiplier['cpc']
            clicks = int(budget_spent / cpc)
            impressions = int(clicks / (random.uniform(0.01, 0.05) * multiplier['ctr']))
            
            # Calculate conversion metrics
            base_conversion_rate = random.uniform(0.01, 0.04) * multiplier['conversion']
            conversions = int(clicks * base_conversion_rate)
            
            # Calculate revenue
            avg_order_value = random.uniform(50, 300)
            revenue = conversions * avg_order_value
            
            # Calculate derived metrics
            click_through_rate = (clicks / impressions) * 100 if impressions > 0 else 0
            conversion_rate = (conversions / clicks) * 100 if clicks > 0 else 0
            engagement_rate = random.uniform(1, 8)
            roi = ((revenue / budget_spent) - 1) * 100 if budget_spent > 0 else 0
            
            campaign = {
                'campaign_id': f'CMP_{i+1:03d}',
                'campaign_name': f'{channel.title()} {random.choice(self.campaign_types).title()} Campaign {i+1}',
                'channel': channel,
                'campaign_type': random.choice(self.campaign_types),
                'start_date': datetime.now() - timedelta(days=random.randint(1, date_range)),
                'budget_allocated': budget_allocated,
                'budget_spent': round(budget_spent, 2),
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'revenue': round(revenue, 2),
                'click_through_rate': round(click_through_rate, 2),
                'conversion_rate': round(conversion_rate, 2),
                'engagement_rate': round(engagement_rate, 2),
                'cost_per_click': round(cpc, 2),
                'cost_per_acquisition': round(budget_spent / conversions, 2) if conversions > 0 else 0,
                'roi': round(roi, 2),
                'target_audience': random.choice(self.customer_segments),
                'status': random.choice(['active', 'paused', 'completed'])
            }
            
            campaigns.append(campaign)
        
        return pd.DataFrame(campaigns)
    
    def _generate_customers(self, num_customers):
        """Generate customer data"""
        customers = []
        
        for i in range(num_customers):
            age = random.randint(18, 70)
            
            # Age-based income and behavior patterns
            if age < 25:  # Gen Z
                income_range = (25000, 45000)
                preferred_channels = ['social_media', 'video']
                engagement_base = 7
            elif age < 40:  # Millennials
                income_range = (35000, 75000)
                preferred_channels = ['search', 'social_media', 'email']
                engagement_base = 6
            elif age < 55:  # Gen X
                income_range = (45000, 95000)
                preferred_channels = ['search', 'email', 'display']
                engagement_base = 5
            else:  # Baby Boomers
                income_range = (40000, 80000)
                preferred_channels = ['email', 'search']
                engagement_base = 4
            
            income = random.randint(*income_range)
            ltv_multiplier = income / 50000  # Higher income = higher LTV
            
            customer = {
                'customer_id': f'CUST_{i+1:06d}',
                'age': age,
                'income': income,
                'preferred_channel': random.choice(preferred_channels),
                'acquisition_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'lifetime_value': round(random.uniform(100, 1000) * ltv_multiplier, 2),
                'total_purchases': random.randint(1, 10),
                'engagement_score': round(random.uniform(1, 10) * (engagement_base/5), 1),
                'segment': self._assign_customer_segment(age),
                'location': random.choice(['US-East', 'US-West', 'US-Central', 'US-South']),
                'device_preference': random.choice(['mobile', 'desktop', 'tablet'])
            }
            
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def _generate_daily_metrics(self, date_range):
        """Generate daily performance metrics"""
        daily_metrics = []
        
        for i in range(date_range):
            date = datetime.now() - timedelta(days=date_range - i - 1)
            
            # Add weekly and seasonal patterns
            day_of_week = date.weekday()
            weekend_multiplier = 0.7 if day_of_week >= 5 else 1.0
            
            # Simulate some growth trend
            growth_factor = 1 + (i / date_range) * 0.2
            
            base_revenue = random.uniform(5000, 15000) * weekend_multiplier * growth_factor
            base_conversions = random.uniform(50, 150) * weekend_multiplier * growth_factor
            base_spend = random.uniform(3000, 8000) * weekend_multiplier
            
            daily_metric = {
                'date': date.date(),
                'revenue': round(base_revenue, 2),
                'conversions': int(base_conversions),
                'spend': round(base_spend, 2),
                'impressions': random.randint(50000, 200000),
                'clicks': random.randint(2000, 8000),
                'conversion_rate': round((base_conversions / random.randint(2000, 8000)) * 100, 2),
                'roi': round(((base_revenue / base_spend) - 1) * 100, 2),
                'day_of_week': date.strftime('%A')
            }
            
            daily_metrics.append(daily_metric)
        
        return pd.DataFrame(daily_metrics)
    
    def _generate_customer_interactions(self, campaigns_df, customers_df, num_interactions):
        """Generate customer interaction data"""
        interactions = []
        
        for i in range(num_interactions):
            campaign = campaigns_df.sample(n=1).iloc[0]
            customer = customers_df.sample(n=1).iloc[0]
            
            # Higher probability of interaction if channel matches preference
            interaction_probability = 0.8 if campaign['channel'] == customer['preferred_channel'] else 0.3
            
            if random.random() < interaction_probability:
                interaction_type = random.choice(['impression', 'click', 'conversion'])
                
                interaction = {
                    'interaction_id': f'INT_{i+1:06d}',
                    'customer_id': customer['customer_id'],
                    'campaign_id': campaign['campaign_id'],
                    'interaction_type': interaction_type,
                    'timestamp': datetime.now() - timedelta(
                        days=random.randint(1, 30),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    ),
                    'channel': campaign['channel'],
                    'device': customer['device_preference'],
                    'location': customer['location'],
                    'value': random.uniform(10, 500) if interaction_type == 'conversion' else 0
                }
                
                interactions.append(interaction)
        
        return pd.DataFrame(interactions)
    
    def _assign_customer_segment(self, age):
        """Assign customer segment based on age"""
        if age < 25:
            return 'gen_z'
        elif age < 40:
            return 'millennials'
        elif age < 55:
            return 'gen_x'
        else:
            return 'baby_boomers'
    
    def generate_market_trends_data(self, num_trends=10):
        """Generate market trends data"""
        trends = []
        
        trend_categories = ['seasonal', 'competitor', 'economic', 'technology', 'consumer_behavior']
        
        for i in range(num_trends):
            trend = {
                'trend_id': f'TREND_{i+1:03d}',
                'category': random.choice(trend_categories),
                'description': self._generate_trend_description(),
                'impact_score': random.uniform(0.1, 1.0),
                'confidence': random.uniform(0.6, 0.95),
                'start_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'expected_duration': random.randint(7, 180),
                'affected_channels': random.sample(self.channels, random.randint(1, 3)),
                'recommended_action': random.choice([
                    'increase_budget', 'adjust_targeting', 'change_creative', 
                    'pause_campaign', 'explore_new_channels'
                ])
            }
            
            trends.append(trend)
        
        return pd.DataFrame(trends)
    
    def _generate_trend_description(self):
        """Generate realistic trend descriptions"""
        descriptions = [
            "Increased mobile usage during evening hours",
            "Rising cost-per-click in competitive keywords",
            "Growing interest in sustainability-focused messaging",
            "Shift towards video content consumption",
            "Declining email open rates in certain segments",
            "Increased social media engagement on weekends",
            "Growing preference for personalized experiences",
            "Rising importance of user-generated content",
            "Increased sensitivity to data privacy concerns",
            "Growing adoption of voice search technology"
        ]
        
        return random.choice(descriptions)
    
    def add_noise_to_data(self, data, noise_level=0.1):
        """Add realistic noise to data for more authentic simulation"""
        if isinstance(data, pd.DataFrame):
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            
            for col in numeric_columns:
                if col not in ['customer_id', 'campaign_id', 'interaction_id']:  # Don't add noise to IDs
                    noise = np.random.normal(0, data[col].std() * noise_level, len(data))
                    data[col] = np.maximum(data[col] + noise, 0)  # Ensure no negative values
        
        return data
