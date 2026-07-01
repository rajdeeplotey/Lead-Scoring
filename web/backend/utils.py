"""
Utility functions for Flask backend.
"""

import pandas as pd
import numpy as np


def clean_for_json(df):
    """
    Clean DataFrame for JSON serialization by replacing NaN values with None.
    This ensures valid JSON output from pandas DataFrames.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with NaN values replaced by None
    """
    if df is None or df.empty:
        return df
    
    # Replace NaN values with None for valid JSON
    df = df.replace({np.nan: None})
    df = df.where(pd.notnull(df), None)
    
    return df


def clean_dict_for_json(data_dict):
    """
    Clean dictionary for JSON serialization by replacing NaN values with None.
    
    Args:
        data_dict (dict): Input dictionary
        
    Returns:
        dict: Dictionary with NaN values replaced by None
    """
    if data_dict is None:
        return data_dict
    
    def clean_value(value):
        if isinstance(value, dict):
            return {k: clean_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [clean_value(item) for item in value]
        elif isinstance(value, (float, int)) and (value != value):  # Check for NaN
            return None
        elif pd.isna(value):
            return None
        return value
    
    return clean_value(data_dict)
