"""
Rule-based lead scoring engine for B Socio.
Implements a 100-point scoring system across 8 pillars.
"""

import pandas as pd


def get_google_rating_tier(rating):
    """
    Convert Google rating to tier score (0-10 points).
    
    Args:
        rating (float): Google rating (0-5)
        
    Returns:
        int: Tier score
    """
    if rating >= 4.5:
        return 10
    elif rating >= 4.0:
        return 8
    elif rating >= 3.5:
        return 5
    elif rating >= 3.0:
        return 3
    else:
        return 0


def get_review_count_tier(review_count):
    """
    Convert review count to tier score (0-10 points).
    
    Args:
        review_count (int): Number of Google reviews
        
    Returns:
        int: Tier score
    """
    if review_count >= 200:
        return 10
    elif review_count >= 100:
        return 8
    elif review_count >= 50:
        return 5
    elif review_count >= 20:
        return 3
    else:
        return 0


def get_follower_tier(follower_count):
    """
    Convert Instagram follower count to tier score (0-10 points).
    
    Args:
        follower_count (int): Instagram follower count
        
    Returns:
        int: Tier score
    """
    if follower_count >= 5000:
        return 10
    elif follower_count >= 2000:
        return 8
    elif follower_count >= 500:
        return 5
    elif follower_count >= 100:
        return 3
    else:
        return 0


def calculate_google_presence_score(row):
    """
    Calculate Google Presence score (20 points total).
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Google Presence score
    """
    rating_tier = get_google_rating_tier(row['google_rating'])
    review_tier = get_review_count_tier(row['google_reviews_count'])
    return rating_tier + review_tier


def calculate_instagram_activity_score(row):
    """
    Calculate Instagram Activity score (20 points total).
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Instagram Activity score
    """
    active_score = 10 if row['instagram_active'] == 1 else 0
    follower_tier = get_follower_tier(row['instagram_followers'])
    return active_score + follower_tier


def calculate_website_status_score(row):
    """
    Calculate Website Status score (15 points total).
    None=0, Basic=8, Good=15
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Website Status score
    """
    website_status = row.get('website_status_score', row.get('website_status', 0))
    if website_status == 0:  # None
        return 0
    elif website_status == 1:  # Basic
        return 8
    else:  # Good
        return 15


def calculate_whatsapp_availability_score(row):
    """
    Calculate WhatsApp Availability score (15 points total).
    Yes=15, No=0
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: WhatsApp Availability score
    """
    return 15 if row['whatsapp_available'] == 1 else 0


def calculate_menu_catalog_score(row):
    """
    Calculate Menu/Catalog Availability score (10 points total).
    Yes=10, No=0
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Menu/Catalog score
    """
    return 10 if row['menu_catalog_available'] == 1 else 0


def calculate_branding_quality_score(row):
    """
    Calculate Branding Quality score (10 points total).
    Low=2, Medium=6, High=10
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Branding Quality score
    """
    branding_quality = row.get('branding_quality_score', row.get('branding_quality', 0))
    if branding_quality == 0:  # Low
        return 2
    elif branding_quality == 1:  # Medium
        return 6
    else:  # High
        return 10


def calculate_online_ordering_score(row):
    """
    Calculate Online Ordering score (10 points total).
    Yes=10, No=0
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        int: Online Ordering score
    """
    return 10 if row['online_orders_accepted'] == 1 else 0


def calculate_lead_score(row):
    """
    Calculate total lead score (100 points total) across all 8 pillars.
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        dict: Dictionary with individual pillar scores and total score
    """
    scores = {
        'google_presence': calculate_google_presence_score(row),
        'instagram_activity': calculate_instagram_activity_score(row),
        'website_status': calculate_website_status_score(row),
        'whatsapp_availability': calculate_whatsapp_availability_score(row),
        'menu_catalog': calculate_menu_catalog_score(row),
        'branding_quality': calculate_branding_quality_score(row),
        'online_ordering': calculate_online_ordering_score(row)
    }
    
    scores['total_score'] = sum(scores.values())
    return scores


def get_lead_status(total_score):
    """
    Determine lead status based on total score.
    Hot: 75-100, Warm: 45-74, Cold: 0-44
    
    Args:
        total_score (int): Total lead score
        
    Returns:
        str: Lead status (Hot/Warm/Cold)
    """
    if total_score >= 75:
        return 'Hot'
    elif total_score >= 45:
        return 'Warm'
    else:
        return 'Cold'


def detect_weaknesses(scores):
    """
    Detect weaknesses (pillars under 50% of max points).
    
    Args:
        scores (dict): Dictionary of pillar scores
        
    Returns:
        list: List of weaknesses with pillar names and scores
    """
    max_points = {
        'google_presence': 20,
        'instagram_activity': 20,
        'website_status': 15,
        'whatsapp_availability': 15,
        'menu_catalog': 10,
        'branding_quality': 10,
        'online_ordering': 10
    }
    
    weaknesses = []
    for pillar, score in scores.items():
        if pillar in max_points:
            threshold = max_points[pillar] * 0.5  # 50% threshold
            if score < threshold:
                weaknesses.append({
                    'pillar': pillar,
                    'score': score,
                    'max': max_points[pillar],
                    'threshold': threshold
                })
    
    return weaknesses


def map_weakness_to_service(weakness):
    """
    Map a weakness to a B Socio service to pitch.
    
    Args:
        weakness (dict): Weakness dictionary
        
    Returns:
        str: Recommended B Socio service
    """
    pillar = weakness['pillar']
    
    service_mapping = {
        'google_presence': 'Google Business Profile Optimization',
        'instagram_activity': 'Instagram Growth & Content Strategy',
        'website_status': 'Website Development & Optimization',
        'whatsapp_availability': 'WhatsApp Business Setup & Automation',
        'menu_catalog': 'Digital Menu/Catalog Creation',
        'branding_quality': 'Brand Identity & Visual Design',
        'online_ordering': 'E-commerce & Online Ordering System'
    }
    
    return service_mapping.get(pillar, 'General Digital Marketing Consultation')


def generate_personalized_dm(business_name, weakness, service):
    """
    Generate a personalized WhatsApp/Instagram DM based on the biggest weakness.
    
    Args:
        business_name (str): Name of the business
        weakness (dict): Biggest weakness
        service (str): Recommended service
        
    Returns:
        str: Personalized DM message
    """
    pillar = weakness['pillar']
    score = weakness['score']
    max_score = weakness['max']
    
    pillar_names = {
        'google_presence': 'Google Presence',
        'instagram_activity': 'Instagram Activity',
        'website_status': 'Website Status',
        'whatsapp_availability': 'WhatsApp Availability',
        'menu_catalog': 'Menu/Catalog Availability',
        'branding_quality': 'Branding Quality',
        'online_ordering': 'Online Ordering'
    }
    
    pillar_name = pillar_names.get(pillar, pillar)
    
    dm = f"""Hi {business_name}!

I noticed your {pillar_name} could use some improvement (currently at {score}/{max_score}). At B Socio, we specialize in {service} to help businesses like yours stand out online.

Would you be open to a quick chat about how we can help?"""
    
    return dm


def score_business(row):
    """
    Complete scoring pipeline for a single business.
    
    Args:
        row (pd.Series): Business data row
        
    Returns:
        dict: Complete scoring results
    """
    scores = calculate_lead_score(row)
    total_score = scores['total_score']
    status = get_lead_status(total_score)
    weaknesses = detect_weaknesses(scores)
    
    # Map weaknesses to services
    for weakness in weaknesses:
        weakness['service'] = map_weakness_to_service(weakness)
    
    # Generate DM for biggest weakness
    dm = None
    if weaknesses:
        biggest_weakness = max(weaknesses, key=lambda x: x['max'] - x['score'])
        service = map_weakness_to_service(biggest_weakness)
        dm = generate_personalized_dm(row['business_name'], biggest_weakness, service)
    
    return {
        'business_name': row['business_name'],
        'total_score': total_score,
        'status': status,
        'pillar_scores': scores,
        'weaknesses': weaknesses,
        'personalized_dm': dm
    }


def score_dataframe(df):
    """
    Score all businesses in a dataframe.
    
    Args:
        df (pd.DataFrame): Dataframe with business data
        
    Returns:
        pd.DataFrame: Dataframe with scoring results added
    """
    results = []
    
    for _, row in df.iterrows():
        result = score_business(row)
        results.append(result)
    
    # Convert to dataframe
    results_df = pd.DataFrame(results)
    
    # Expand pillar scores into columns
    pillar_scores_df = pd.json_normalize(results_df['pillar_scores'])
    pillar_scores_df.columns = [f'score_{col}' for col in pillar_scores_df.columns]
    
    # Drop business_name from results_df to avoid duplicates (already in df)
    results_df = results_df.drop(['business_name', 'pillar_scores'], axis=1)
    
    # Combine
    final_df = pd.concat([df.reset_index(drop=True), results_df, pillar_scores_df], axis=1)
    
    # Remove any duplicate columns that may have been created
    final_df = final_df.loc[:, ~final_df.columns.duplicated()]
    
    return final_df


if __name__ == "__main__":
    # Test the module
    import os
    from data_prep import prepare_data
    
    test_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_businesses_khanna.csv")
    df = prepare_data(test_file)
    
    # Test single business
    print("Testing single business scoring:")
    result = score_business(df.iloc[0])
    print(f"Business: {result['business_name']}")
    print(f"Total Score: {result['total_score']}/100")
    print(f"Status: {result['status']}")
    print(f"Pillar Scores: {result['pillar_scores']}")
    print(f"Weaknesses: {result['weaknesses']}")
    print(f"\nPersonalized DM:\n{result['personalized_dm']}")
    
    # Test dataframe scoring
    print("\n\nTesting dataframe scoring:")
    scored_df = score_dataframe(df)
    print(f"Scored {len(scored_df)} businesses")
    print("\nScore distribution:")
    print(scored_df['status'].value_counts())
    print("\nFirst few rows with scores:")
    print(scored_df[['business_name', 'total_score', 'status']].head())
