"""
Data preparation module for B Socio Lead Scoring.
Handles safe CSV loading and encoding of categorical variables.
"""

import pandas as pd


def load_csv_safely(file_path):
    """
    Load CSV file with safe NA handling to prevent "None" text from being treated as missing.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataframe with proper data types
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If CSV is empty or malformed
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    
    df = pd.read_csv(
        file_path,
        keep_default_na=False,
        na_values=[]
    )
    
    if df.empty:
        raise ValueError("CSV file is empty")
    
    return df


def encode_yes_no_columns(df):
    """
    Encode Yes/No columns to 1/0.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with encoded Yes/No columns
    """
    yes_no_columns = [
        'phone_available',
        'whatsapp_available',
        'instagram_active',
        'facebook_active',
        'menu_catalog_available',
        'online_orders_accepted'
    ]
    
    for col in yes_no_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
    
    return df


def encode_website_status(df):
    """
    Encode website_status to numeric scores: None=0, Basic=1, Good=2.
    Creates website_status_score column to match ML model training features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with encoded website_status
    """
    if 'website_status' in df.columns:
        df['website_status_score'] = df['website_status'].map({'None': 0, 'Basic': 1, 'Good': 2})
        df = df.drop('website_status', axis=1)
    
    return df


def encode_branding_quality(df):
    """
    Encode branding_quality to numeric scores: Low=0, Medium=1, High=2.
    Creates branding_quality_score column to match ML model training features.
    Empty/None values are left as NaN/None to be handled by scoring engine.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with encoded branding_quality
    """
    if 'branding_quality' in df.columns:
        # Only map non-empty values, leave empty/None as NaN
        df['branding_quality_score'] = df['branding_quality'].apply(
            lambda x: {'Low': 0, 'Medium': 1, 'High': 2}.get(x, None) if pd.notna(x) and x != '' else None
        )
        df = df.drop('branding_quality', axis=1)
    
    return df


def prepare_data(file_path):
    """
    Complete data preparation pipeline: load CSV and encode all categorical variables.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Fully prepared dataframe ready for scoring/ML
    """
    df = load_csv_safely(file_path)
    df = encode_yes_no_columns(df)
    df = encode_website_status(df)
    df = encode_branding_quality(df)
    return df


if __name__ == "__main__":
    # Test the module
    import os
    test_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_businesses_khanna.csv")
    df = prepare_data(test_file)
    print("Data preparation test successful!")
    print(f"Shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
