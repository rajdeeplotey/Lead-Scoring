"""
Streamlit app for B Socio Lead Scoring.
Two tabs: Upload CSV and Manual Entry.
"""

import streamlit as st
import pandas as pd
import io
import os

# Add src to path for imports
import sys
sys.path.insert(0, os.path.dirname(__file__))

from data_prep import prepare_data, encode_yes_no_columns, encode_website_status, encode_branding_quality
from scoring_engine import score_dataframe, score_business
from ml_model import add_ml_predictions


st.set_page_config(
    page_title="B Socio Lead Scoring",
    page_icon="📊",
    layout="wide"
)

st.title("B Socio AI Lead Scoring")
st.markdown("Score businesses based on their digital presence and get actionable insights.")


def display_score_card(result):
    """
    Display a score card for a single business.
    
    Args:
        result (dict): Scoring result dictionary
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Score", f"{result['total_score']}/100")
    
    with col2:
        status_color = {
            'Hot': '🔥',
            'Warm': '🌡️',
            'Cold': '❄️'
        }
        st.metric("Status", f"{status_color.get(result['status'], '')} {result['status']}")
    
    with col3:
        st.metric("Weaknesses Found", len(result['weaknesses']))
    
    st.subheader("Pillar Scores")
    pillar_scores = result['pillar_scores']
    
    # Create progress bars for each pillar
    max_points = {
        'google_presence': 20,
        'instagram_activity': 20,
        'website_status': 15,
        'whatsapp_availability': 15,
        'menu_catalog': 10,
        'branding_quality': 10,
        'online_ordering': 10
    }
    
    for pillar, score in pillar_scores.items():
        if pillar != 'total_score':
            max_val = max_points.get(pillar, 10)
            st.progress(score / max_val)
            st.caption(f"{pillar.replace('_', ' ').title()}: {score}/{max_val}")
    
    if result['weaknesses']:
        st.subheader("Detected Weaknesses")
        for weakness in result['weaknesses']:
            with st.expander(f"{weakness['pillar'].replace('_', ' ').title()} - {weakness['score']}/{weakness['max']}"):
                st.write(f"**Service to Pitch:** {weakness['service']}")
                st.write(f"Score: {weakness['score']}/{weakness['max']} (Threshold: {weakness['threshold']})")
    
    if result['personalized_dm']:
        st.subheader("Personalized DM")
        st.text_area("Copy this message:", result['personalized_dm'], height=120)


def upload_csv_tab():
    """
    Upload CSV tab - upload a businesses CSV, show scored table with download.
    """
    st.header("Upload CSV")
    st.markdown("Upload a CSV file with business data to get lead scores for all businesses.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file, keep_default_na=False, na_values=[])
            st.success(f"Loaded {len(df)} businesses from CSV")
            
            # Validate required columns
            required_columns = [
                'business_name', 'phone_available', 'whatsapp_available',
                'instagram_active', 'instagram_followers', 'facebook_active',
                'website_status', 'google_rating', 'google_reviews_count',
                'menu_catalog_available', 'branding_quality', 'years_in_business',
                'online_orders_accepted'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                st.markdown("""
                **Required columns:**
                - business_name, phone_available, whatsapp_available
                - instagram_active, instagram_followers, facebook_active
                - website_status, google_rating, google_reviews_count
                - menu_catalog_available, branding_quality
                - years_in_business, online_orders_accepted
                """)
                return
            
            # Prepare data using individual encoding functions
            df_prepared = encode_yes_no_columns(df)
            df_prepared = encode_website_status(df_prepared)
            df_prepared = encode_branding_quality(df_prepared)
            
            # Score with rule-based engine
            df_scored = score_dataframe(df_prepared)
            
            # Add ML predictions
            try:
                df_scored = add_ml_predictions(df_scored)
                st.info("ML predictions added successfully")
            except Exception as e:
                st.warning(f"ML predictions not available: {e}")
            
            # Display scored table
            st.subheader("Scored Businesses")
            
            # Select columns to display
            display_cols = ['business_name', 'total_score', 'status', 'ml_lead_score', 'ml_lead_status']
            available_cols = [col for col in display_cols if col in df_scored.columns]
            
            if 'ml_lead_score' not in df_scored.columns:
                available_cols = ['business_name', 'total_score', 'status']
            
            display_df = df_scored[available_cols].copy()
            
            # Reset index and remove duplicate columns to fix styling errors
            display_df = display_df.reset_index(drop=True)
            display_df = display_df.loc[:, ~display_df.columns.duplicated()]
            
            # Add color coding for status
            def color_status(val):
                if val == 'Hot':
                    return 'background-color: #ffcccc'
                elif val == 'Warm':
                    return 'background-color: #ffffcc'
                else:
                    return 'background-color: #ccccff'
            
            try:
                styled_df = display_df.style.map(color_status, subset=['status'])
                st.dataframe(styled_df, use_container_width=True)
            except Exception:
                # Fallback to plain dataframe if styling fails
                st.dataframe(display_df, use_container_width=True)
            
            # Download button
            csv = df_scored.to_csv(index=False)
            st.download_button(
                label="Download Scored CSV",
                data=csv,
                file_name="scored_businesses.csv",
                mime="text/csv"
            )
            
            # Business detail view
            st.subheader("Business Details")
            if 'business_name' in df_scored.columns:
                # Safe implementation to handle potential duplicate columns
                business_names = df_scored['business_name']
                
                if isinstance(business_names, pd.DataFrame):
                    business_names = business_names.iloc[:, 0]
                
                business_names = (
                    business_names
                    .dropna()
                    .astype(str)
                    .drop_duplicates()
                    .sort_values()
                    .tolist()
                )
                
                selected_business = st.selectbox(
                    "Select a business to view details",
                    options=business_names
                )
                
                if selected_business:
                    business_row = df_scored[df_scored['business_name'] == selected_business].iloc[0]
                    
                    # Get weaknesses from the original scoring
                    original_df = encode_yes_no_columns(df)
                    original_df = encode_website_status(original_df)
                    original_df = encode_branding_quality(original_df)
                    original_row = original_df[original_df['business_name'] == selected_business].iloc[0]
                    result = score_business(original_row)
                    
                    display_score_card(result)
            
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.exception(e)
    
    else:
        st.info("Please upload a CSV file to begin.")
        st.markdown("""
        **Expected CSV format:**
        - business_id, business_name, category, location
        - phone_available, whatsapp_available, instagram_active, facebook_active (Yes/No)
        - instagram_followers (number)
        - website_status (None/Basic/Good)
        - google_rating (0-5), google_reviews_count (number)
        - menu_catalog_available, online_orders_accepted (Yes/No)
        - branding_quality (Low/Medium/High)
        - years_in_business (number)
        """)


def manual_entry_tab():
    """
    Manual Entry tab - form to enter one business's details and get instant score card.
    """
    st.header("Manual Entry")
    st.markdown("Enter a business's details manually to get an instant lead score.")
    
    with st.form("business_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Business Name*", value="")
            category = st.text_input("Category", value="")
            location = st.text_input("Location", value="")
            
            st.subheader("Contact & Social")
            phone_available = st.selectbox("Phone Available", ["Yes", "No"])
            whatsapp_available = st.selectbox("WhatsApp Available", ["Yes", "No"])
            instagram_active = st.selectbox("Instagram Active", ["Yes", "No"])
            instagram_followers = st.number_input("Instagram Followers", min_value=0, value=0)
            facebook_active = st.selectbox("Facebook Active", ["Yes", "No"])
        
        with col2:
            st.subheader("Digital Presence")
            website_status = st.selectbox("Website Status", ["None", "Basic", "Good"])
            google_rating = st.slider("Google Rating", 0.0, 5.0, 3.5, 0.1)
            google_reviews_count = st.number_input("Google Reviews Count", min_value=0, value=0)
            menu_catalog_available = st.selectbox("Menu/Catalog Available", ["Yes", "No"])
            branding_quality = st.selectbox("Branding Quality", ["Low", "Medium", "High"])
            years_in_business = st.number_input("Years in Business", min_value=0, value=1)
            online_orders_accepted = st.selectbox("Online Orders Accepted", ["Yes", "No"])
        
        submitted = st.form_submit_button("Calculate Score")
        
        if submitted and business_name:
            # Create dataframe from form data
            data = {
                'business_id': [1],
                'business_name': [business_name],
                'category': [category],
                'location': [location],
                'phone_available': [phone_available],
                'whatsapp_available': [whatsapp_available],
                'instagram_active': [instagram_active],
                'instagram_followers': [instagram_followers],
                'facebook_active': [facebook_active],
                'website_status': [website_status],
                'google_rating': [google_rating],
                'google_reviews_count': [google_reviews_count],
                'menu_catalog_available': [menu_catalog_available],
                'branding_quality': [branding_quality],
                'years_in_business': [years_in_business],
                'online_orders_accepted': [online_orders_accepted]
            }
            
            df = pd.DataFrame(data)
            
            # Prepare and score
            df_prepared = prepare_data_from_dict(data)
            result = score_business(df_prepared.iloc[0])
            
            st.success("Score calculated successfully!")
            display_score_card(result)


def prepare_data_from_dict(data_dict):
    """
    Prepare data from a dictionary (for manual entry).
    
    Args:
        data_dict (dict): Dictionary with business data
        
    Returns:
        pd.DataFrame: Prepared dataframe
    """
    df = pd.DataFrame(data_dict)
    
    # Encode Yes/No columns
    yes_no_columns = [
        'phone_available', 'whatsapp_available', 'instagram_active',
        'facebook_active', 'menu_catalog_available', 'online_orders_accepted'
    ]
    
    for col in yes_no_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
    
    # Encode website_status
    if 'website_status' in df.columns:
        df['website_status_score'] = df['website_status'].map({'None': 0, 'Basic': 1, 'Good': 2})
        df = df.drop('website_status', axis=1)
    
    # Encode branding_quality
    if 'branding_quality' in df.columns:
        df['branding_quality_score'] = df['branding_quality'].map({'Low': 0, 'Medium': 1, 'High': 2})
        df = df.drop('branding_quality', axis=1)
    
    return df


# Main app
tab1, tab2 = st.tabs(["Upload CSV", "Manual Entry"])

with tab1:
    upload_csv_tab()

with tab2:
    manual_entry_tab()

# Footer
st.markdown("---")
st.markdown("Powered by B Socio AI Lead Scoring Engine")
