import pandas as pd
import numpy as np
from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class BudgetOptimizer:
    """AI Agent for optimizing budget allocation across campaigns"""
    
    def __init__(self):
        self.roi_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def optimize_budget_allocation(self, campaign_data, total_budget, optimization_goal='roi'):
        """Optimize budget allocation across campaigns"""
        campaigns_df = campaign_data['campaigns'].copy()
        
        # Train predictive models if not already trained
        if not self.is_trained:
            self._train_models(campaigns_df)
        
        # Get current campaign performance
        current_performance = self._calculate_current_performance(campaigns_df)
        
        # Optimize budget allocation
        optimal_allocation = self._optimize_allocation(
            campaigns_df, total_budget, optimization_goal
        )
        
        # Calculate expected results
        expected_results = self._calculate_expected_results(
            optimal_allocation, campaigns_df, optimization_goal
        )
        
        # Generate recommendations
        recommendations = self._generate_budget_recommendations(
            current_performance, optimal_allocation, campaigns_df
        )
        
        return {
            'optimal_allocation': optimal_allocation,
            'expected_results': expected_results,
            'current_performance': current_performance,
            'recommendations': recommendations,
            'improvement_potential': self._calculate_improvement_potential(
                current_performance, expected_results
            )
        }
    
    def _train_models(self, campaigns_df):
        """Train predictive models for budget optimization"""
        # Prepare features for ROI prediction
        feature_columns = ['budget_spent', 'impressions', 'clicks', 'click_through_rate']
        X = campaigns_df[feature_columns].fillna(0)
        y = campaigns_df['revenue'] / campaigns_df['budget_spent']  # Revenue ratio
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train ROI predictor
        self.roi_predictor.fit(X_scaled, y)
        self.is_trained = True
    
    def _calculate_current_performance(self, campaigns_df):
        """Calculate current performance metrics"""
        return {
            'total_spend': campaigns_df['budget_spent'].sum(),
            'total_revenue': campaigns_df['revenue'].sum(),
            'total_conversions': campaigns_df['conversions'].sum(),
            'avg_roi': ((campaigns_df['revenue'].sum() / campaigns_df['budget_spent'].sum()) - 1) * 100,
            'campaign_count': len(campaigns_df)
        }
    
    def _optimize_allocation(self, campaigns_df, total_budget, goal):
        """Optimize budget allocation using mathematical optimization"""
        n_campaigns = len(campaigns_df)
        
        # Initialize with equal allocation
        initial_allocation = np.full(n_campaigns, total_budget / n_campaigns)
        
        # Define constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - total_budget},  # Budget constraint
            {'type': 'ineq', 'fun': lambda x: x}  # Non-negative constraint
        ]
        
        # Set bounds (minimum 5% of total budget per campaign, maximum 40%)
        bounds = [(total_budget * 0.05, total_budget * 0.4) for _ in range(n_campaigns)]
        
        # Define objective function based on goal
        if goal == 'roi':
            objective = lambda x: -self._calculate_total_roi(x, campaigns_df)
        elif goal == 'revenue':
            objective = lambda x: -self._calculate_total_revenue(x, campaigns_df)
        elif goal == 'conversions':
            objective = lambda x: -self._calculate_total_conversions(x, campaigns_df)
        else:
            objective = lambda x: -self._calculate_total_reach(x, campaigns_df)
        
        # Optimize
        result = minimize(
            objective, 
            initial_allocation, 
            method='SLSQP', 
            bounds=bounds, 
            constraints=constraints
        )
        
        # Create allocation result
        allocation_result = []
        for i, budget in enumerate(result.x):
            campaign = campaigns_df.iloc[i]
            allocation_result.append({
                'campaign_name': campaign['campaign_name'],
                'channel': campaign['channel'],
                'current_budget': campaign['budget_spent'],
                'optimal_budget': budget,
                'budget_change': budget - campaign['budget_spent'],
                'budget_change_pct': ((budget - campaign['budget_spent']) / campaign['budget_spent']) * 100
            })
        
        return allocation_result
    
    def _calculate_total_roi(self, budget_allocation, campaigns_df):
        """Calculate total ROI for given budget allocation"""
        total_revenue = 0
        total_spend = 0
        
        for i, budget in enumerate(budget_allocation):
            campaign = campaigns_df.iloc[i]
            predicted_revenue = self._predict_campaign_revenue(campaign, budget)
            total_revenue += predicted_revenue
            total_spend += budget
        
        return (total_revenue / total_spend - 1) * 100 if total_spend > 0 else 0
    
    def _calculate_total_revenue(self, budget_allocation, campaigns_df):
        """Calculate total revenue for given budget allocation"""
        total_revenue = 0
        
        for i, budget in enumerate(budget_allocation):
            campaign = campaigns_df.iloc[i]
            predicted_revenue = self._predict_campaign_revenue(campaign, budget)
            total_revenue += predicted_revenue
        
        return total_revenue
    
    def _calculate_total_conversions(self, budget_allocation, campaigns_df):
        """Calculate total conversions for given budget allocation"""
        total_conversions = 0
        
        for i, budget in enumerate(budget_allocation):
            campaign = campaigns_df.iloc[i]
            # Estimate conversions based on budget and historical performance
            budget_ratio = budget / campaign['budget_spent'] if campaign['budget_spent'] > 0 else 1
            predicted_conversions = campaign['conversions'] * (budget_ratio ** 0.8)  # Diminishing returns
            total_conversions += predicted_conversions
        
        return total_conversions
    
    def _calculate_total_reach(self, budget_allocation, campaigns_df):
        """Calculate total reach for given budget allocation"""
        total_reach = 0
        
        for i, budget in enumerate(budget_allocation):
            campaign = campaigns_df.iloc[i]
            # Estimate reach based on budget and historical performance
            budget_ratio = budget / campaign['budget_spent'] if campaign['budget_spent'] > 0 else 1
            predicted_reach = campaign['impressions'] * (budget_ratio ** 0.9)  # Near-linear scaling
            total_reach += predicted_reach
        
        return total_reach
    
    def _predict_campaign_revenue(self, campaign, new_budget):
        """Predict campaign revenue for new budget allocation"""
        # Simple prediction based on historical performance with diminishing returns
        if campaign['budget_spent'] > 0:
            budget_ratio = new_budget / campaign['budget_spent']
            # Apply diminishing returns (square root relationship)
            predicted_revenue = campaign['revenue'] * (budget_ratio ** 0.7)
        else:
            # If no historical data, use industry average
            predicted_revenue = new_budget * 2.5  # Assuming 2.5x revenue ratio
        
        return max(predicted_revenue, 0)
    
    def _calculate_expected_results(self, optimal_allocation, campaigns_df, goal):
        """Calculate expected results from optimal allocation"""
        total_budget = sum([alloc['optimal_budget'] for alloc in optimal_allocation])
        total_revenue = 0
        total_conversions = 0
        
        for i, allocation in enumerate(optimal_allocation):
            campaign = campaigns_df.iloc[i]
            predicted_revenue = self._predict_campaign_revenue(campaign, allocation['optimal_budget'])
            
            # Estimate conversions
            budget_ratio = allocation['optimal_budget'] / campaign['budget_spent'] if campaign['budget_spent'] > 0 else 1
            predicted_conversions = campaign['conversions'] * (budget_ratio ** 0.8)
            
            total_revenue += predicted_revenue
            total_conversions += predicted_conversions
        
        roi = (total_revenue / total_budget - 1) * 100 if total_budget > 0 else 0
        
        return {
            'total_budget': total_budget,
            'revenue': total_revenue,
            'conversions': total_conversions,
            'roi': roi
        }
    
    def _generate_budget_recommendations(self, current_performance, optimal_allocation, campaigns_df):
        """Generate actionable budget recommendations"""
        recommendations = []
        
        # Identify campaigns with significant budget changes
        for allocation in optimal_allocation:
            change_pct = allocation['budget_change_pct']
            
            if change_pct > 25:
                recommendations.append(
                    f"Increase budget for '{allocation['campaign_name']}' by {change_pct:.1f}% - high ROI potential"
                )
            elif change_pct < -25:
                recommendations.append(
                    f"Reduce budget for '{allocation['campaign_name']}' by {abs(change_pct):.1f}% - low efficiency"
                )
        
        # Channel-level recommendations
        channel_changes = {}
        for allocation in optimal_allocation:
            channel = allocation['channel']
            if channel not in channel_changes:
                channel_changes[channel] = 0
            channel_changes[channel] += allocation['budget_change']
        
        for channel, change in channel_changes.items():
            if change > 5000:
                recommendations.append(f"Increase investment in {channel} channel by ${change:,.0f}")
            elif change < -5000:
                recommendations.append(f"Reduce investment in {channel} channel by ${abs(change):,.0f}")
        
        if not recommendations:
            recommendations.append("Current budget allocation is near-optimal")
        
        return recommendations
    
    def _calculate_improvement_potential(self, current, expected):
        """Calculate improvement potential from optimization"""
        roi_improvement = expected['roi'] - current['avg_roi']
        revenue_improvement = expected['revenue'] - current['total_revenue']
        conversion_improvement = expected['conversions'] - current['total_conversions']
        
        return {
            'roi_improvement': roi_improvement,
            'revenue_improvement': revenue_improvement,
            'conversion_improvement': conversion_improvement,
            'revenue_improvement_pct': (revenue_improvement / current['total_revenue']) * 100 if current['total_revenue'] > 0 else 0
        }
    
    def simulate_budget_scenarios(self, campaign_data, budget_range):
        """Simulate different budget scenarios"""
        scenarios = []
        
        for budget in budget_range:
            result = self.optimize_budget_allocation(campaign_data, budget, 'roi')
            scenarios.append({
                'budget': budget,
                'expected_roi': result['expected_results']['roi'],
                'expected_revenue': result['expected_results']['revenue']
            })
        
        return scenarios
