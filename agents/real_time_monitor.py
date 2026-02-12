import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class RealTimeMonitor:
    """AI Agent for real-time campaign monitoring and alerting"""
    
    def __init__(self):
        self.alert_thresholds = {
            'roi_critical': -10,  # ROI below -10%
            'roi_warning': 20,    # ROI below 20%
            'conversion_rate_low': 1.0,  # Conversion rate below 1%
            'cpc_high': 10.0,     # CPC above $10
            'budget_burn_rate': 0.8,  # 80% of budget spent
            'traffic_drop': 0.5   # 50% traffic drop
        }
        
        self.notification_history = []
        
    def monitor_campaigns(self, campaign_data):
        """Monitor campaigns for anomalies and performance issues"""
        campaigns_df = campaign_data['campaigns']
        alerts = []
        
        for idx, campaign in campaigns_df.iterrows():
            campaign_alerts = self._check_campaign_health(campaign)
            alerts.extend(campaign_alerts)
        
        # System-wide alerts
        system_alerts = self._check_system_health(campaigns_df)
        alerts.extend(system_alerts)
        
        return {
            'alerts': alerts,
            'alert_summary': self._generate_alert_summary(alerts),
            'recommendations': self._generate_alert_recommendations(alerts),
            'health_score': self._calculate_system_health_score(campaigns_df)
        }
    
    def _check_campaign_health(self, campaign):
        """Check individual campaign health"""
        alerts = []
        campaign_name = campaign['campaign_name']
        
        # ROI alerts
        if campaign['roi'] < self.alert_thresholds['roi_critical']:
            alerts.append({
                'type': 'critical',
                'category': 'ROI',
                'campaign': campaign_name,
                'message': f"Critical: ROI is {campaign['roi']:.1f}% (below {self.alert_thresholds['roi_critical']}%)",
                'action': 'immediate_review',
                'timestamp': datetime.now()
            })
        elif campaign['roi'] < self.alert_thresholds['roi_warning']:
            alerts.append({
                'type': 'warning',
                'category': 'ROI',
                'campaign': campaign_name,
                'message': f"Warning: ROI is {campaign['roi']:.1f}% (below target {self.alert_thresholds['roi_warning']}%)",
                'action': 'optimization_needed',
                'timestamp': datetime.now()
            })
        
        # Conversion rate alerts
        if campaign['conversion_rate'] < self.alert_thresholds['conversion_rate_low']:
            alerts.append({
                'type': 'warning',
                'category': 'Conversion',
                'campaign': campaign_name,
                'message': f"Low conversion rate: {campaign['conversion_rate']:.2f}%",
                'action': 'improve_landing_page',
                'timestamp': datetime.now()
            })
        
        # Cost per click alerts
        if campaign['cost_per_click'] > self.alert_thresholds['cpc_high']:
            alerts.append({
                'type': 'warning',
                'category': 'CPC',
                'campaign': campaign_name,
                'message': f"High CPC: ${campaign['cost_per_click']:.2f}",
                'action': 'optimize_bidding',
                'timestamp': datetime.now()
            })
        
        # Budget burn rate
        budget_used_pct = (campaign['budget_spent'] / campaign['budget_allocated']) if campaign['budget_allocated'] > 0 else 0
        if budget_used_pct > self.alert_thresholds['budget_burn_rate']:
            alerts.append({
                'type': 'info',
                'category': 'Budget',
                'campaign': campaign_name,
                'message': f"Budget {budget_used_pct*100:.1f}% utilized",
                'action': 'monitor_spending',
                'timestamp': datetime.now()
            })
        
        return alerts
    
    def _check_system_health(self, campaigns_df):
        """Check overall system health"""
        alerts = []
        
        # Overall performance metrics
        total_spend = campaigns_df['budget_spent'].sum()
        total_revenue = campaigns_df['revenue'].sum()
        overall_roi = (total_revenue / total_spend - 1) * 100 if total_spend > 0 else 0
        
        if overall_roi < 0:
            alerts.append({
                'type': 'critical',
                'category': 'System',
                'campaign': 'All Campaigns',
                'message': f"System-wide negative ROI: {overall_roi:.1f}%",
                'action': 'portfolio_review',
                'timestamp': datetime.now()
            })
        
        # Channel performance alerts
        channel_performance = campaigns_df.groupby('channel')['roi'].mean()
        for channel, roi in channel_performance.items():
            if roi < 0:
                alerts.append({
                    'type': 'warning',
                    'category': 'Channel',
                    'campaign': f'{channel.title()} Channel',
                    'message': f"Channel showing negative ROI: {roi:.1f}%",
                    'action': 'channel_optimization',
                    'timestamp': datetime.now()
                })
        
        return alerts
    
    def _generate_alert_summary(self, alerts):
        """Generate summary of alerts"""
        alert_counts = {'critical': 0, 'warning': 0, 'info': 0}
        
        for alert in alerts:
            alert_counts[alert['type']] += 1
        
        return {
            'total_alerts': len(alerts),
            'critical_alerts': alert_counts['critical'],
            'warning_alerts': alert_counts['warning'],
            'info_alerts': alert_counts['info'],
            'needs_immediate_attention': alert_counts['critical'] > 0
        }
    
    def _generate_alert_recommendations(self, alerts):
        """Generate actionable recommendations based on alerts"""
        recommendations = []
        
        # Group alerts by action type
        action_groups = {}
        for alert in alerts:
            action = alert['action']
            if action not in action_groups:
                action_groups[action] = []
            action_groups[action].append(alert)
        
        # Generate recommendations for each action group
        for action, action_alerts in action_groups.items():
            if action == 'immediate_review':
                campaigns = [alert['campaign'] for alert in action_alerts]
                recommendations.append({
                    'priority': 'high',
                    'action': 'Immediate Review Required',
                    'description': f"Campaigns with critical ROI issues: {', '.join(campaigns)}",
                    'suggested_steps': [
                        'Pause underperforming campaigns',
                        'Analyze traffic sources and targeting',
                        'Review creative performance',
                        'Consider budget reallocation'
                    ]
                })
            
            elif action == 'optimization_needed':
                recommendations.append({
                    'priority': 'medium',
                    'action': 'Campaign Optimization',
                    'description': f"{len(action_alerts)} campaigns need performance optimization",
                    'suggested_steps': [
                        'A/B test new creative variations',
                        'Refine audience targeting',
                        'Optimize bidding strategies',
                        'Improve landing page conversion'
                    ]
                })
            
            elif action == 'improve_landing_page':
                recommendations.append({
                    'priority': 'medium',
                    'action': 'Landing Page Optimization',
                    'description': f"{len(action_alerts)} campaigns have low conversion rates",
                    'suggested_steps': [
                        'A/B test landing page elements',
                        'Improve page load speed',
                        'Enhance call-to-action buttons',
                        'Simplify conversion funnel'
                    ]
                })
        
        return recommendations
    
    def _calculate_system_health_score(self, campaigns_df):
        """Calculate overall system health score (0-100)"""
        health_factors = []
        
        # ROI factor
        avg_roi = ((campaigns_df['revenue'].sum() / campaigns_df['budget_spent'].sum()) - 1) * 100
        roi_score = min(max((avg_roi + 50) / 150 * 100, 0), 100)  # Normalize ROI to 0-100
        health_factors.append(roi_score * 0.4)  # 40% weight
        
        # Conversion rate factor
        total_conversions = campaigns_df['conversions'].sum()
        total_clicks = campaigns_df['clicks'].sum()
        avg_conversion_rate = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0
        conversion_score = min(avg_conversion_rate * 25, 100)  # 4% conversion = 100 points
        health_factors.append(conversion_score * 0.25)  # 25% weight
        
        # Diversity factor (more channels = better)
        channel_diversity = campaigns_df['channel'].nunique()
        diversity_score = min(channel_diversity * 25, 100)  # 4+ channels = 100 points
        health_factors.append(diversity_score * 0.2)  # 20% weight
        
        # Performance consistency factor
        roi_std = campaigns_df['roi'].std()
        roi_mean = campaigns_df['roi'].mean()
        consistency_score = max(100 - (roi_std / max(abs(roi_mean), 1) * 100), 0)
        health_factors.append(consistency_score * 0.15)  # 15% weight
        
        return sum(health_factors)
    
    def generate_performance_alerts(self, campaign_data, previous_data=None):
        """Generate alerts based on performance changes"""
        alerts = []
        
        if previous_data is None:
            return alerts
        
        current_campaigns = campaign_data['campaigns']
        previous_campaigns = previous_data['campaigns']
        
        # Compare performance metrics
        for idx, current_campaign in current_campaigns.iterrows():
            campaign_name = current_campaign['campaign_name']
            previous_campaign = previous_campaigns[
                previous_campaigns['campaign_name'] == campaign_name
            ]
            
            if not previous_campaign.empty:
                prev_roi = previous_campaign.iloc[0]['roi']
                current_roi = current_campaign['roi']
                roi_change = current_roi - prev_roi
                
                if roi_change < -20:  # ROI dropped by more than 20%
                    alerts.append({
                        'type': 'warning',
                        'category': 'Performance Decline',
                        'campaign': campaign_name,
                        'message': f"ROI declined by {abs(roi_change):.1f}% (from {prev_roi:.1f}% to {current_roi:.1f}%)",
                        'action': 'investigate_decline',
                        'timestamp': datetime.now()
                    })
        
        return alerts
    
    def get_notification_settings(self):
        """Get current notification settings"""
        return {
            'alert_thresholds': self.alert_thresholds,
            'notification_methods': ['dashboard', 'email', 'slack'],
            'alert_frequency': 'real_time',
            'escalation_rules': {
                'critical_alerts': 'immediate',
                'warning_alerts': 'hourly',
                'info_alerts': 'daily'
            }
        }
    
    def update_alert_thresholds(self, new_thresholds):
        """Update alert thresholds"""
        self.alert_thresholds.update(new_thresholds)
        return True