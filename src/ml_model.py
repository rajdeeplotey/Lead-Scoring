"""
ML model module for B Socio Lead Scoring.
Loads trained models and predicts lead scores and status.
"""

import joblib
import pandas as pd
import os


class LeadScoringModel:
    """
    Wrapper class for lead scoring ML models.
    """
    
    def __init__(self, model_dir=None):
        """
        Initialize the model loader.
        
        Args:
            model_dir (str): Directory containing model files. 
                           Defaults to ../models relative to this file.
        """
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        
        self.model_dir = model_dir
        self.lead_score_model = None
        self.lead_status_classifier = None
        self._load_models()
    
    def _load_models(self):
        """
        Load the trained ML models from disk.
        """
        score_model_path = os.path.join(self.model_dir, "lead_score_model.pkl")
        status_model_path = os.path.join(self.model_dir, "lead_status_classifier.pkl")
        
        try:
            self.lead_score_model = joblib.load(score_model_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Lead score model not found at {score_model_path}")
        except Exception as e:
            raise RuntimeError(f"Error loading lead score model: {e}")
        
        try:
            self.lead_status_classifier = joblib.load(status_model_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Lead status classifier not found at {status_model_path}")
        except Exception as e:
            raise RuntimeError(f"Error loading lead status classifier: {e}")
    
    def predict_lead_score(self, df):
        """
        Predict ML lead score for businesses.
        
        Args:
            df (pd.DataFrame): Dataframe with encoded business features
            
        Returns:
            np.ndarray: Predicted lead scores
        """
        if self.lead_score_model is None:
            raise ValueError("Lead score model not loaded")
        
        # Select features expected by the model (must match training features)
        feature_columns = [
            'whatsapp_available', 'instagram_active', 'instagram_followers',
            'facebook_active', 'website_status_score', 'google_rating',
            'google_reviews_count', 'menu_catalog_available',
            'branding_quality_score', 'years_in_business', 'online_orders_accepted'
        ]
        
        # Ensure all features exist
        missing_features = [col for col in feature_columns if col not in df.columns]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        X = df[feature_columns]
        predictions = self.lead_score_model.predict(X)
        return predictions
    
    def predict_lead_status(self, df):
        """
        Predict ML lead status for businesses.
        
        Args:
            df (pd.DataFrame): Dataframe with encoded business features
            
        Returns:
        np.ndarray: Predicted lead status labels
        """
        if self.lead_status_classifier is None:
            raise ValueError("Lead status classifier not loaded")
        
        # Select features expected by the model (must match training features)
        feature_columns = [
            'whatsapp_available', 'instagram_active', 'instagram_followers',
            'facebook_active', 'website_status_score', 'google_rating',
            'google_reviews_count', 'menu_catalog_available',
            'branding_quality_score', 'years_in_business', 'online_orders_accepted'
        ]
        
        # Ensure all features exist
        missing_features = [col for col in feature_columns if col not in df.columns]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        X = df[feature_columns]
        predictions = self.lead_status_classifier.predict(X)
        return predictions
    
    def predict(self, df):
        """
        Predict both lead score and status for businesses.
        
        Args:
            df (pd.DataFrame): Dataframe with encoded business features
            
        Returns:
            tuple: (lead_scores, lead_statuses)
        """
        lead_scores = self.predict_lead_score(df)
        lead_statuses = self.predict_lead_status(df)
        return lead_scores, lead_statuses


def add_ml_predictions(df, model_dir=None):
    """
    Add ML predictions to a dataframe.
    
    Args:
        df (pd.DataFrame): Dataframe with encoded business features
        model_dir (str): Directory containing model files
        
    Returns:
        pd.DataFrame: Dataframe with ml_lead_score and ml_lead_status columns added
    """
    model = LeadScoringModel(model_dir)
    
    lead_scores, lead_statuses = model.predict(df)
    
    df = df.copy()
    df['ml_lead_score'] = lead_scores
    df['ml_lead_status'] = lead_statuses
    
    return df


if __name__ == "__main__":
    # Test the module
    from data_prep import prepare_data
    
    test_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_businesses_khanna.csv")
    df = prepare_data(test_file)
    
    print("Testing ML model predictions:")
    print(f"Input data shape: {df.shape}")
    
    try:
        model = LeadScoringModel()
        
        # Test predictions
        lead_scores = model.predict_lead_score(df)
        lead_statuses = model.predict_lead_status(df)
        
        print(f"\nPredicted lead scores for first 5 businesses:")
        for i, score in enumerate(lead_scores[:5]):
            print(f"  {df.iloc[i]['business_name']}: {score:.2f}")
        
        print(f"\nPredicted lead statuses for first 5 businesses:")
        for i, status in enumerate(lead_statuses[:5]):
            print(f"  {df.iloc[i]['business_name']}: {status}")
        
        # Test adding predictions to dataframe
        df_with_ml = add_ml_predictions(df)
        print(f"\nDataframe with ML predictions shape: {df_with_ml.shape}")
        print("\nColumns added:", ['ml_lead_score', 'ml_lead_status'])
        print("\nSample rows with ML predictions:")
        print(df_with_ml[['business_name', 'ml_lead_score', 'ml_lead_status']].head())
        
    except Exception as e:
        print(f"Error during ML model testing: {e}")
        print("This is expected if model files don't exist yet.")
