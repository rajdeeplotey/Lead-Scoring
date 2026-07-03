"""
Flask backend for B Socio AI Lead Scoring System.
Provides REST API endpoints for lead scoring.
"""

import os
import sys
import io
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path for imports
# In Vercel, the working directory is the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from data_prep import encode_yes_no_columns, encode_website_status, encode_branding_quality
from scoring_engine import score_dataframe, score_business
from ml_model import add_ml_predictions

# Try relative import for package mode (Vercel), fall back to absolute for direct execution
try:
    from .utils import clean_for_json, clean_dict_for_json
except ImportError:
    from utils import clean_for_json, clean_dict_for_json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

CORS(app)

# Paths - work in both local and Vercel environments
# Get project root by going up from app.py location
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
SAMPLE_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'sample_businesses_khanna.csv')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'web', 'frontend')
FRONTEND_URL = os.getenv('FRONTEND_URL', '')


def prepare_data_from_csv(csv_content):
    """
    Prepare data from CSV content for scoring.
    
    Args:
        csv_content: CSV file content (string or file-like object)
        
    Returns:
        pd.DataFrame: Prepared dataframe
    """
    df = pd.read_csv(csv_content, keep_default_na=False, na_values=[])
    df = encode_yes_no_columns(df)
    df = encode_website_status(df)
    df = encode_branding_quality(df)
    return df


def prepare_data_from_dict(data_dict):
    """
    Prepare data from dictionary for scoring.
    
    Args:
        data_dict (dict): Business data dictionary
        
    Returns:
        pd.DataFrame: Prepared dataframe
    """
    logger.debug(f"prepare_data_from_dict received: {data_dict}")
    df = pd.DataFrame([data_dict])
    logger.debug(f"DataFrame columns before encoding: {df.columns.tolist()}")
    logger.debug(f"DataFrame values before encoding:\n{df.to_string()}")
    
    # Encode Yes/No columns
    yes_no_columns = [
        'phone_available', 'whatsapp_available', 'instagram_active',
        'facebook_active', 'menu_catalog_available', 'online_orders_accepted'
    ]
    
    for col in yes_no_columns:
        if col in df.columns:
            logger.debug(f"Encoding {col}: {df[col].values}")
            df[col] = df[col].map({'Yes': 1, 'No': 0})
            logger.debug(f"After encoding {col}: {df[col].values}")
    
    # Encode website_status
    if 'website_status' in df.columns:
        logger.debug(f"Encoding website_status: {df['website_status'].values}")
        df['website_status_score'] = df['website_status'].map({'None': 0, 'Basic': 1, 'Good': 2})
        df = df.drop('website_status', axis=1)
        logger.debug(f"After encoding website_status_score: {df['website_status_score'].values}")
    
    # Encode branding_quality
    if 'branding_quality' in df.columns:
        logger.debug(f"Encoding branding_quality: {df['branding_quality'].values}")
        # Only map non-empty values, leave empty/None as NaN
        df['branding_quality_score'] = df['branding_quality'].apply(
            lambda x: {'Low': 0, 'Medium': 1, 'High': 2}.get(x, None) if pd.notna(x) and x != '' else None
        )
        df = df.drop('branding_quality', axis=1)
        logger.debug(f"After encoding branding_quality_score: {df['branding_quality_score'].values}")
    
    return df


@app.route('/api/score-csv', methods=['POST'])
def score_csv():
    """
    Score businesses from uploaded CSV file.
    
    Expected: multipart/form-data with 'file' field containing CSV
    Returns: JSON with scored businesses
    """
    try:
        logger.info("Received CSV upload request")
        
        if 'file' not in request.files:
            logger.warning("No file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        logger.info(f"File received: {file.filename}")
        
        if file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'File must be a CSV'}), 400
        
        # Read and prepare data
        logger.info("Reading and preparing CSV data...")
        df = prepare_data_from_csv(file)
        logger.info(f"CSV loaded with {len(df)} rows")
        
        # Score with rule-based engine
        logger.info("Scoring with rule-based engine...")
        df_scored = score_dataframe(df)
        logger.info("Scoring completed")
        
        # Add ML predictions
        try:
            logger.info("Adding ML predictions...")
            df_scored = add_ml_predictions(df_scored)
            logger.info("ML predictions added successfully")
        except Exception as e:
            # ML predictions are optional
            logger.warning(f"ML predictions not available: {e}")
        
        # Convert to JSON-serializable format
        logger.info("Converting to JSON...")
        # Clean DataFrame for JSON serialization
        df_scored = clean_for_json(df_scored)
        result = df_scored.to_dict(orient='records')
        logger.info(f"Converted {len(result)} records")
        
        return jsonify({
            'success': True,
            'count': len(result),
            'businesses': result
        })
    
    except Exception as e:
        logger.error(f"Error in score_csv: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/score-manual', methods=['POST'])
def score_manual():
    """
    Score a single business from JSON data.
    
    Expected: JSON with business fields
    Returns: JSON with score, status, weaknesses, service, and DM
    """
    try:
        data = request.get_json()
        
        logger.info(f"Received manual scoring request for: {data.get('business_name', 'Unknown')}")
        logger.debug(f"Instagram followers: {data.get('instagram_followers')}")
        logger.debug(f"Years in business: {data.get('years_in_business')}")
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'business_name', 'phone_available', 'whatsapp_available',
            'instagram_active', 'instagram_followers', 'facebook_active',
            'website_status', 'google_rating', 'google_reviews_count',
            'menu_catalog_available', 'branding_quality', 'years_in_business',
            'online_orders_accepted'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Prepare and score
        df_prepared = prepare_data_from_dict(data)
        result = score_business(df_prepared.iloc[0])
        
        logger.info(f"Scoring result - Total score: {result.get('total_score')}, Status: {result.get('status')}")
        
        # Clean result for JSON serialization
        result = clean_dict_for_json(result)
        
        # Add timestamp to ensure fresh response
        import time
        result['_timestamp'] = time.time()
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """
    Get sample business data as JSON.
    
    Returns: JSON with sample businesses
    """
    try:
        if not os.path.exists(SAMPLE_DATA_PATH):
            return jsonify({'error': 'Sample data file not found'}), 404
        
        df = pd.read_csv(SAMPLE_DATA_PATH, keep_default_na=False, na_values=[])
        # Clean DataFrame for JSON serialization
        df = clean_for_json(df)
        result = df.to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'count': len(result),
            'businesses': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


# Serve frontend files
@app.route('/')
def index():
    """Serve the index.html page."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/static/<path:filename>')
def serve_static_files(filename):
    """Serve static files from the static directory."""
    static_dir = os.path.join(FRONTEND_DIR, 'static')
    return send_from_directory(static_dir, filename)


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images, etc.)."""
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
