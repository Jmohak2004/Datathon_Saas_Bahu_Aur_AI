import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, accuracy_score, silhouette_score
import warnings
warnings.filterwarnings('ignore')

class MLModelSuite:
    """Suite of machine learning models for campaign optimization"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.is_trained = {}
        
        # Initialize models
        self.models['roi_predictor'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['conversion_predictor'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.models['churn_predictor'] = LogisticRegression(random_state=42)
        self.models['ltv_predictor'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['customer_segmentation'] = KMeans(n_clusters=4, random_state=42)
        
        # Initialize scalers and encoders
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()
            self.encoders[model_name] = LabelEncoder()
            self.is_trained[model_name] = False
    
    def train_roi_predictor(self, campaign_data):
        """Train ROI prediction model"""
        campaigns_df = campaign_data['campaigns'].copy()
        
        # Prepare features
        feature_columns = ['budget_spent', 'impressions', 'clicks', 'click_through_rate', 'engagement_rate']
        X = campaigns_df[feature_columns].fillna(0)
        y = campaigns_df['roi']
        
        # Scale features
        X_scaled = self.scalers['roi_predictor'].fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Train model
        self.models['roi_predictor'].fit(X_train, y_train)
        self.is_trained['roi_predictor'] = True
        
        # Evaluate model
        train_score = self.models['roi_predictor'].score(X_train, y_train)
        test_score = self.models['roi_predictor'].score(X_test, y_test)
        
        return {
            'train_score': train_score,
            'test_score': test_score,
            'feature_importance': dict(zip(feature_columns, self.models['roi_predictor'].feature_importances_))
        }
    
    def train_conversion_predictor(self, campaign_data):
        """Train conversion rate prediction model"""
        campaigns_df = campaign_data['campaigns'].copy()
        
        # Prepare features
        feature_columns = ['budget_spent', 'impressions', 'clicks', 'click_through_rate', 'engagement_rate']
        X = campaigns_df[feature_columns].fillna(0)
        y = campaigns_df['conversion_rate']
        
        # Scale features
        X_scaled = self.scalers['conversion_predictor'].fit_transform(X)
        
        # Train model
        self.models['conversion_predictor'].fit(X_scaled, y)
        self.is_trained['conversion_predictor'] = True
        
        # Cross-validation score
        cv_scores = cross_val_score(self.models['conversion_predictor'], X_scaled, y, cv=5)
        
        return {
            'cv_mean_score': cv_scores.mean(),
            'cv_std_score': cv_scores.std(),
            'feature_importance': dict(zip(feature_columns, self.models['conversion_predictor'].feature_importances_))
        }
    
    def train_customer_segmentation(self, campaign_data):
        """Train customer segmentation model"""
        customers_df = campaign_data['customers'].copy()
        
        # Prepare features for clustering
        feature_columns = ['age', 'income', 'lifetime_value', 'engagement_score', 'total_purchases']
        X = customers_df[feature_columns].fillna(0)
        
        # Scale features
        X_scaled = self.scalers['customer_segmentation'].fit_transform(X)
        
        # Train clustering model
        clusters = self.models['customer_segmentation'].fit_predict(X_scaled)
        customers_df['segment'] = clusters
        
        self.is_trained['customer_segmentation'] = True
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(X_scaled, clusters)
        
        # Analyze segments
        segment_analysis = self._analyze_customer_segments(customers_df, feature_columns)
        
        return {
            'silhouette_score': silhouette_avg,
            'segment_analysis': segment_analysis,
            'cluster_centers': self.models['customer_segmentation'].cluster_centers_
        }
    
    def train_ltv_predictor(self, campaign_data):
        """Train customer lifetime value prediction model"""
        customers_df = campaign_data['customers'].copy()
        
        # Prepare features
        feature_columns = ['age', 'income', 'engagement_score', 'total_purchases']
        X = customers_df[feature_columns].fillna(0)
        y = customers_df['lifetime_value']
        
        # Scale features
        X_scaled = self.scalers['ltv_predictor'].fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Train model
        self.models['ltv_predictor'].fit(X_train, y_train)
        self.is_trained['ltv_predictor'] = True
        
        # Evaluate
        y_pred = self.models['ltv_predictor'].predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = self.models['ltv_predictor'].score(X_test, y_test)
        
        return {
            'mse': mse,
            'r2_score': r2,
            'feature_importance': dict(zip(feature_columns, self.models['ltv_predictor'].feature_importances_))
        }
    
    def train_churn_predictor(self, campaign_data):
        """Train customer churn prediction model"""
        customers_df = campaign_data['customers'].copy()
        
        # Create churn labels (synthetic for demo)
        # Customers with low engagement and old acquisition dates are more likely to churn
        days_since_acquisition = (pd.Timestamp.now() - customers_df['acquisition_date']).dt.days
        churn_probability = (days_since_acquisition / 365) * (1 / customers_df['engagement_score'])
        customers_df['churned'] = (churn_probability > np.percentile(churn_probability, 75)).astype(int)
        
        # Prepare features
        feature_columns = ['age', 'income', 'engagement_score', 'total_purchases']
        X = customers_df[feature_columns].fillna(0)
        y = customers_df['churned']
        
        # Scale features
        X_scaled = self.scalers['churn_predictor'].fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Train model
        self.models['churn_predictor'].fit(X_train, y_train)
        self.is_trained['churn_predictor'] = True
        
        # Evaluate
        y_pred = self.models['churn_predictor'].predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get feature importance (coefficients for logistic regression)
        feature_importance = dict(zip(feature_columns, abs(self.models['churn_predictor'].coef_[0])))
        
        return {
            'accuracy': accuracy,
            'feature_importance': feature_importance,
            'churn_rate': y.mean()
        }
    
    def predict_campaign_roi(self, campaign_features):
        """Predict ROI for new campaign"""
        if not self.is_trained['roi_predictor']:
            raise ValueError("ROI predictor not trained yet")
        
        # Scale features
        features_scaled = self.scalers['roi_predictor'].transform([campaign_features])
        
        # Make prediction
        prediction = self.models['roi_predictor'].predict(features_scaled)[0]
        
        # Get prediction confidence (using ensemble variance)
        predictions = [tree.predict(features_scaled)[0] for tree in self.models['roi_predictor'].estimators_]
        confidence = 1 - (np.std(predictions) / np.mean(predictions)) if np.mean(predictions) != 0 else 0
        
        return {
            'predicted_roi': prediction,
            'confidence': min(max(confidence, 0), 1),  # Clamp between 0 and 1
            'prediction_range': (np.min(predictions), np.max(predictions))
        }
    
    def predict_customer_ltv(self, customer_features):
        """Predict customer lifetime value"""
        if not self.is_trained['ltv_predictor']:
            raise ValueError("LTV predictor not trained yet")
        
        # Scale features
        features_scaled = self.scalers['ltv_predictor'].transform([customer_features])
        
        # Make prediction
        prediction = self.models['ltv_predictor'].predict(features_scaled)[0]
        
        return max(prediction, 0)  # Ensure non-negative LTV
    
    def predict_churn_probability(self, customer_features):
        """Predict customer churn probability"""
        if not self.is_trained['churn_predictor']:
            raise ValueError("Churn predictor not trained yet")
        
        # Scale features
        features_scaled = self.scalers['churn_predictor'].transform([customer_features])
        
        # Get probability
        probability = self.models['churn_predictor'].predict_proba(features_scaled)[0][1]
        
        return probability
    
    def segment_customer(self, customer_features):
        """Assign customer to segment"""
        if not self.is_trained['customer_segmentation']:
            raise ValueError("Customer segmentation not trained yet")
        
        # Scale features
        features_scaled = self.scalers['customer_segmentation'].transform([customer_features])
        
        # Predict segment
        segment = self.models['customer_segmentation'].predict(features_scaled)[0]
        
        return segment
    
    def optimize_campaign_parameters(self, target_roi, budget_range):
        """Optimize campaign parameters for target ROI"""
        if not self.is_trained['roi_predictor']:
            raise ValueError("ROI predictor not trained yet")
        
        best_params = None
        best_roi = float('-inf')
        
        # Grid search over parameter space
        for budget in np.linspace(budget_range[0], budget_range[1], 20):
            for ctr in np.linspace(0.01, 0.05, 10):
                for engagement in np.linspace(1, 10, 10):
                    # Estimate impressions and clicks based on budget and CTR
                    estimated_cpc = 2.0  # Average CPC
                    estimated_clicks = budget / estimated_cpc
                    estimated_impressions = estimated_clicks / ctr
                    
                    features = [budget, estimated_impressions, estimated_clicks, ctr * 100, engagement]
                    prediction_result = self.predict_campaign_roi(features)
                    predicted_roi = prediction_result['predicted_roi']
                    
                    if predicted_roi >= target_roi and predicted_roi > best_roi:
                        best_roi = predicted_roi
                        best_params = {
                            'budget': budget,
                            'target_ctr': ctr,
                            'target_engagement': engagement,
                            'estimated_roi': predicted_roi,
                            'confidence': prediction_result['confidence']
                        }
        
        return best_params
    
    def get_model_performance_summary(self):
        """Get summary of all model performances"""
        summary = {}
        
        for model_name, trained in self.is_trained.items():
            summary[model_name] = {
                'trained': trained,
                'model_type': type(self.models[model_name]).__name__
            }
        
        return summary
    
    def _analyze_customer_segments(self, customers_df, feature_columns):
        """Analyze customer segments"""
        segment_analysis = {}
        
        for segment in customers_df['segment'].unique():
            segment_data = customers_df[customers_df['segment'] == segment]
            
            analysis = {
                'size': len(segment_data),
                'percentage': len(segment_data) / len(customers_df) * 100,
                'avg_age': segment_data['age'].mean(),
                'avg_income': segment_data['income'].mean(),
                'avg_ltv': segment_data['lifetime_value'].mean(),
                'avg_engagement': segment_data['engagement_score'].mean(),
                'preferred_channels': segment_data['preferred_channel'].mode().tolist(),
                'characteristics': self._generate_segment_characteristics(segment_data)
            }
            
            segment_analysis[f'Segment_{segment}'] = analysis
        
        return segment_analysis
    
    def _generate_segment_characteristics(self, segment_data):
        """Generate characteristics description for a segment"""
        avg_age = segment_data['age'].mean()
        avg_income = segment_data['income'].mean()
        avg_engagement = segment_data['engagement_score'].mean()
        
        characteristics = []
        
        # Age characteristics
        if avg_age < 30:
            characteristics.append("Young demographics")
        elif avg_age < 45:
            characteristics.append("Middle-aged professionals")
        else:
            characteristics.append("Mature audience")
        
        # Income characteristics
        if avg_income > 70000:
            characteristics.append("High income")
        elif avg_income > 40000:
            characteristics.append("Middle income")
        else:
            characteristics.append("Budget-conscious")
        
        # Engagement characteristics
        if avg_engagement > 7:
            characteristics.append("Highly engaged")
        elif avg_engagement > 5:
            characteristics.append("Moderately engaged")
        else:
            characteristics.append("Low engagement")
        
        return characteristics
    
    def retrain_all_models(self, campaign_data):
        """Retrain all models with new data"""
        results = {}
        
        try:
            results['roi_predictor'] = self.train_roi_predictor(campaign_data)
            results['conversion_predictor'] = self.train_conversion_predictor(campaign_data)
            results['customer_segmentation'] = self.train_customer_segmentation(campaign_data)
            results['ltv_predictor'] = self.train_ltv_predictor(campaign_data)
            results['churn_predictor'] = self.train_churn_predictor(campaign_data)
            
            results['retrain_status'] = 'success'
        except Exception as e:
            results['retrain_status'] = 'error'
            results['error_message'] = str(e)
        
        return results
