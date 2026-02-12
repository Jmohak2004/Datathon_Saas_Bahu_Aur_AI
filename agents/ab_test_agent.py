import pandas as pd
import numpy as np
from scipy import stats
import math
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ABTestAgent:
    """AI Agent for A/B testing recommendations and analysis"""
    
    def __init__(self):
        self.test_history = []
        self.significance_level = 0.05
        
    def suggest_ab_tests(self, campaign_data):
        """Suggest A/B tests based on campaign performance"""
        campaigns_df = campaign_data['campaigns']
        
        suggestions = []
        
        # Analyze campaign performance to identify test opportunities
        test_opportunities = self._identify_test_opportunities(campaigns_df)
        
        for opportunity in test_opportunities:
            suggestion = self._create_test_suggestion(opportunity, campaigns_df)
            suggestions.append(suggestion)
        
        return {
            'suggestions': suggestions,
            'priority_tests': self._prioritize_tests(suggestions),
            'test_calendar': self._create_test_calendar(suggestions)
        }
    
    def analyze_test_results(self, campaign_data):
        """Analyze A/B test results and provide statistical significance"""
        # Simulate some A/B test results for demonstration
        test_results = {}
        
        # Create mock A/B test scenarios
        test_scenarios = [
            {
                'name': 'Landing Page Headline Test',
                'control_rate': 2.3,
                'variant_rate': 2.8,
                'sample_size': 5000
            },
            {
                'name': 'CTA Button Color Test',
                'control_rate': 1.8,
                'variant_rate': 2.1,
                'sample_size': 3500
            },
            {
                'name': 'Ad Creative Test',
                'control_rate': 3.2,
                'variant_rate': 3.0,
                'sample_size': 4200
            },
            {
                'name': 'Email Subject Line Test',
                'control_rate': 4.1,
                'variant_rate': 4.8,
                'sample_size': 6000
            }
        ]
        
        for test in test_scenarios:
            result = self._calculate_statistical_significance(
                test['control_rate'], 
                test['variant_rate'], 
                test['sample_size']
            )
            
            test_results[test['name']] = {
                'control_rate': test['control_rate'],
                'variant_rate': test['variant_rate'],
                'lift': ((test['variant_rate'] / test['control_rate']) - 1) * 100,
                'significant': result['significant'],
                'p_value': result['p_value'],
                'confidence_interval': result['confidence_interval'],
                'sample_size': test['sample_size'],
                'recommendation': self._generate_test_recommendation(result, test)
            }
        
        return test_results
    
    def calculate_sample_size(self, baseline_rate=0.02, minimum_effect=0.20, 
                            confidence_level=0.95, power=0.8):
        """Calculate required sample size for A/B test"""
        # Convert percentage to decimal if needed
        if baseline_rate > 1:
            baseline_rate = baseline_rate / 100
        if minimum_effect > 1:
            minimum_effect = minimum_effect / 100
        
        # Calculate effect size
        variant_rate = baseline_rate * (1 + minimum_effect)
        
        # Calculate pooled standard error
        pooled_rate = (baseline_rate + variant_rate) / 2
        pooled_se = math.sqrt(2 * pooled_rate * (1 - pooled_rate))
        
        # Calculate z-scores
        z_alpha = stats.norm.ppf(1 - (1 - confidence_level) / 2)
        z_beta = stats.norm.ppf(power)
        
        # Calculate sample size per variant
        effect_size = abs(variant_rate - baseline_rate)
        sample_size_per_variant = ((z_alpha + z_beta) * pooled_se / effect_size) ** 2
        
        return int(math.ceil(sample_size_per_variant))
    
    def create_test_plan(self, test_name, hypothesis, variants, success_metric):
        """Create a detailed A/B test plan"""
        sample_size = self.calculate_sample_size()
        
        test_plan = {
            'test_name': test_name,
            'hypothesis': hypothesis,
            'variants': variants,
            'success_metric': success_metric,
            'sample_size_per_variant': sample_size,
            'estimated_duration': self._estimate_test_duration(sample_size),
            'significance_level': self.significance_level,
            'power': 0.8,
            'test_setup': self._generate_test_setup_instructions(variants),
            'analysis_plan': self._generate_analysis_plan(success_metric)
        }
        
        return test_plan
    
    def monitor_test_progress(self, test_data):
        """Monitor ongoing A/B test progress"""
        control_data = test_data['control']
        variant_data = test_data['variant']
        
        # Calculate current metrics
        control_rate = control_data['conversions'] / control_data['visitors']
        variant_rate = variant_data['conversions'] / variant_data['visitors']
        
        # Check if we have enough data for preliminary analysis
        min_sample_size = 1000  # Minimum sample size for preliminary check
        
        progress = {
            'control_visitors': control_data['visitors'],
            'variant_visitors': variant_data['visitors'],
            'control_rate': control_rate * 100,
            'variant_rate': variant_rate * 100,
            'current_lift': ((variant_rate / control_rate) - 1) * 100 if control_rate > 0 else 0,
            'progress_percentage': min(control_data['visitors'] / min_sample_size * 100, 100),
            'ready_for_analysis': control_data['visitors'] >= min_sample_size and variant_data['visitors'] >= min_sample_size
        }
        
        # Provide recommendations based on progress
        if progress['ready_for_analysis']:
            significance_result = self._calculate_statistical_significance(
                control_rate * 100, variant_rate * 100, control_data['visitors']
            )
            progress['preliminary_significant'] = significance_result['significant']
            progress['preliminary_p_value'] = significance_result['p_value']
        
        return progress
    
    def _identify_test_opportunities(self, campaigns_df):
        """Identify potential A/B test opportunities"""
        opportunities = []
        
        # Low conversion rate campaigns
        low_conversion_campaigns = campaigns_df[
            campaigns_df['conversion_rate'] < campaigns_df['conversion_rate'].median()
        ]
        
        for idx, campaign in low_conversion_campaigns.iterrows():
            opportunities.append({
                'type': 'conversion_optimization',
                'campaign': campaign['campaign_name'],
                'current_rate': campaign['conversion_rate'],
                'potential_impact': 'high',
                'test_areas': ['landing_page', 'cta', 'headline']
            })
        
        # High traffic, low engagement campaigns
        high_traffic_campaigns = campaigns_df[
            (campaigns_df['impressions'] > campaigns_df['impressions'].quantile(0.75)) &
            (campaigns_df['engagement_rate'] < campaigns_df['engagement_rate'].median())
        ]
        
        for idx, campaign in high_traffic_campaigns.iterrows():
            opportunities.append({
                'type': 'engagement_optimization',
                'campaign': campaign['campaign_name'],
                'current_engagement': campaign['engagement_rate'],
                'potential_impact': 'medium',
                'test_areas': ['creative', 'messaging', 'audience']
            })
        
        # Channel optimization opportunities
        channel_performance = campaigns_df.groupby('channel').agg({
            'conversion_rate': 'mean',
            'click_through_rate': 'mean',
            'roi': 'mean'
        }).reset_index()
        
        underperforming_channels = channel_performance[
            channel_performance['roi'] < channel_performance['roi'].median()
        ]
        
        for idx, channel in underperforming_channels.iterrows():
            opportunities.append({
                'type': 'channel_optimization',
                'channel': channel['channel'],
                'current_roi': channel['roi'],
                'potential_impact': 'high',
                'test_areas': ['targeting', 'bidding', 'creative']
            })
        
        return opportunities
    
    def _create_test_suggestion(self, opportunity, campaigns_df):
        """Create detailed test suggestion from opportunity"""
        test_suggestions = {
            'conversion_optimization': {
                'test_name': f"Conversion Rate Optimization - {opportunity.get('campaign', 'Unknown Campaign')}",
                'hypothesis': "Improving landing page design and CTA will increase conversion rates",
                'variable': 'Landing Page Elements',
                'expected_impact': '15-25% conversion rate improvement',
                'duration': '14 days',
                'sample_size': 2000
            },
            'engagement_optimization': {
                'test_name': f"Engagement Optimization - {opportunity.get('campaign', 'Unknown Campaign')}",
                'hypothesis': "More compelling creative and messaging will increase engagement",
                'variable': 'Ad Creative and Copy',
                'expected_impact': '10-20% engagement improvement',
                'duration': '10 days',
                'sample_size': 3000
            },
            'channel_optimization': {
                'test_name': f"Channel Strategy Test - {opportunity.get('channel', opportunity.get('campaign', 'Unknown'))}",
                'hypothesis': "Optimized targeting and bidding will improve ROI",
                'variable': 'Targeting Parameters',
                'expected_impact': '20-30% ROI improvement',
                'duration': '21 days',
                'sample_size': 5000
            }
        }
        
        return test_suggestions.get(opportunity['type'], test_suggestions['conversion_optimization'])
    
    def _calculate_statistical_significance(self, control_rate, variant_rate, sample_size):
        """Calculate statistical significance of A/B test results"""
        # Convert percentages to decimals
        if control_rate > 1:
            control_rate = control_rate / 100
        if variant_rate > 1:
            variant_rate = variant_rate / 100
        
        # Calculate conversions
        control_conversions = int(control_rate * sample_size)
        variant_conversions = int(variant_rate * sample_size)
        
        # Perform two-proportion z-test
        pooled_rate = (control_conversions + variant_conversions) / (2 * sample_size)
        pooled_se = math.sqrt(pooled_rate * (1 - pooled_rate) * (2 / sample_size))
        
        if pooled_se == 0:
            return {
                'significant': False,
                'p_value': 1.0,
                'confidence_interval': (0, 0)
            }
        
        z_score = (variant_rate - control_rate) / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        # Calculate confidence interval for the difference
        diff = variant_rate - control_rate
        margin_of_error = stats.norm.ppf(0.975) * pooled_se
        confidence_interval = (diff - margin_of_error, diff + margin_of_error)
        
        return {
            'significant': p_value < self.significance_level,
            'p_value': p_value,
            'z_score': z_score,
            'confidence_interval': confidence_interval
        }
    
    def _generate_test_recommendation(self, result, test_data):
        """Generate recommendation based on test results"""
        if result['significant']:
            if test_data['variant_rate'] > test_data['control_rate']:
                return "✅ Implement variant - statistically significant improvement"
            else:
                return "❌ Keep control - variant performed significantly worse"
        else:
            return "⚠️ No significant difference - consider running longer or testing different variables"
    
    def _prioritize_tests(self, suggestions):
        """Prioritize A/B tests based on potential impact and effort"""
        priority_scores = []
        
        for suggestion in suggestions:
            # Simple scoring based on expected impact and duration
            impact_score = {'high': 3, 'medium': 2, 'low': 1}.get(
                suggestion.get('expected_impact', '').split('-')[0].strip(), 1
            )
            
            duration = int(suggestion.get('duration', '14').split()[0])
            effort_score = 3 if duration <= 7 else 2 if duration <= 14 else 1
            
            priority_score = impact_score * effort_score
            priority_scores.append((suggestion, priority_score))
        
        # Sort by priority score (descending)
        prioritized = sorted(priority_scores, key=lambda x: x[1], reverse=True)
        
        return [test[0] for test in prioritized[:5]]  # Return top 5
    
    def _create_test_calendar(self, suggestions):
        """Create a testing calendar"""
        calendar = []
        start_date = datetime.now()
        
        for i, suggestion in enumerate(suggestions[:6]):  # Limit to 6 tests
            duration = int(suggestion.get('duration', '14').split()[0])
            test_start = start_date + timedelta(days=i * 7)  # Stagger tests by 1 week
            test_end = test_start + timedelta(days=duration)
            
            calendar.append({
                'test_name': suggestion['test_name'],
                'start_date': test_start.strftime('%Y-%m-%d'),
                'end_date': test_end.strftime('%Y-%m-%d'),
                'duration': duration,
                'status': 'planned'
            })
        
        return calendar
    
    def _estimate_test_duration(self, sample_size, daily_traffic=1000):
        """Estimate test duration based on sample size and traffic"""
        days_needed = math.ceil((sample_size * 2) / daily_traffic)  # *2 for both variants
        return max(days_needed, 7)  # Minimum 7 days
    
    def _generate_test_setup_instructions(self, variants):
        """Generate test setup instructions"""
        instructions = []
        instructions.append("1. Set up equal traffic split (50/50) between variants")
        instructions.append("2. Ensure random assignment of users to variants")
        instructions.append("3. Set up conversion tracking for primary success metric")
        instructions.append("4. Configure secondary metrics tracking")
        instructions.append("5. Set up automated data collection")
        
        return instructions
    
    def _generate_analysis_plan(self, success_metric):
        """Generate analysis plan for A/B test"""
        plan = {
            'primary_metric': success_metric,
            'secondary_metrics': ['engagement_rate', 'bounce_rate', 'time_on_page'],
            'segmentation_analysis': ['device_type', 'traffic_source', 'user_type'],
            'statistical_tests': ['two_proportion_z_test', 'chi_square_test'],
            'significance_level': self.significance_level,
            'minimum_sample_size': 1000
        }
        
        return plan
