# B Socio AI Lead Scoring Web Application

A full-stack web application for AI-powered lead scoring with Flask backend and modern HTML/Tailwind CSS frontend. This system helps businesses evaluate potential leads based on their digital presence across multiple platforms.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Architecture](#architecture)
- [Scoring System](#scoring-system)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Frontend Pages](#frontend-pages)
- [Data Flow](#data-flow)
- [Performance Optimizations](#performance-optimizations)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Overview

B Socio Lead Scoring is a comprehensive system that evaluates businesses based on their digital footprint across 8 key pillars:

1. **Google Presence** (20 points) - Google rating and review count
2. **Instagram Activity** (20 points) - Account activity and follower count
3. **Website Status** (15 points) - Website quality and functionality
4. **WhatsApp Availability** (15 points) - WhatsApp business account presence
5. **Menu/Catalog** (10 points) - Digital menu or catalog availability
6. **Branding Quality** (10 points) - Brand identity and visual design
7. **Online Ordering** (10 points) - E-commerce capabilities

Each business receives a total score (0-100) and is classified as:
- **Hot Lead** (75-100): High potential, ready for immediate outreach
- **Warm Lead** (45-74): Moderate potential, needs nurturing
- **Cold Lead** (0-44): Low potential, requires significant improvement

## Project Structure

```
B-Socio-Lead-Scoring/
├── data/                          # Sample data files
│   └── sample_businesses_khanna.csv
├── models/                        # ML model files
│   ├── lead_score_model.pkl
│   └── lead_status_classifier.pkl
├── src/                           # Core scoring logic
│   ├── app.py                     # Main application entry
│   ├── data_prep.py               # Data preparation and encoding
│   ├── scoring_engine.py         # Rule-based scoring engine
│   └── ml_model.py                # ML prediction model wrapper
├── web/                           # Web application
│   ├── backend/
│   │   ├── app.py                 # Flask API server
│   │   ├── utils.py               # Utility functions
│   │   └── requirements.txt       # Python dependencies
│   └── frontend/
│       ├── index.html             # Landing page
│       ├── upload.html            # CSV upload page
│       ├── manual-entry.html      # Manual business entry form
│       ├── dashboard.html         # Analytics dashboard
│       ├── navbar.html            # Shared navigation component
│       ├── footer.html            # Shared footer component
│       ├── styles.css             # Custom styles
│       └── [images]               # Static assets
├── .env                           # Environment variables
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── start.bat                      # Windows startup script
```

## Features

### Backend (Flask)

**Core Endpoints:**
- **POST /api/score-csv** - Upload CSV file, score all businesses with rule-based and ML predictions
- **POST /api/score-manual** - Score single business from JSON data with live preview
- **GET /api/sample-data** - Get sample business data for testing
- **GET /health** - Health check endpoint
- **GET /** - Serve frontend index page
- **GET /<path>** - Serve static frontend files

**Technical Features:**
- CORS enabled for cross-origin frontend communication
- Reuses existing scoring logic from `src/` directory
- Graceful fallback when ML models are unavailable
- JSON serialization utilities for NaN handling
- Comprehensive error handling and logging

### Frontend (HTML/Tailwind/JS)

**Pages:**
- **index.html** - Modern landing page with hero section, feature highlights, and call-to-action
- **upload.html** - Drag-and-drop CSV upload with real-time processing and results table
- **manual-entry.html** - Interactive form with live score preview, pillar breakdown, and weakness detection
- **dashboard.html** - Analytics dashboard with Chart.js visualizations (status distribution, category scores, weaknesses)

**Technical Features:**
- Fully responsive design (mobile-first approach)
- Shared navbar with mobile hamburger menu
- LocalStorage for data persistence across page navigation
- Live preview with debounced API calls (400ms) for performance
- Throttled scroll events (16ms) for smooth scrolling
- GPU-accelerated CSS transitions with `will-change` hints
- Chart.js optimizations with 500ms animations
- Loading states with spinners
- Error handling with friendly messages
- Modal system for detailed business views

## Architecture

### Data Flow

```
User Input → Frontend → API Request → Flask Backend → Scoring Engine → ML Model → Response → Frontend Display
```

### Component Interaction

1. **Frontend** captures user input (CSV upload or manual form)
2. **Flask API** receives requests and validates data
3. **Data Prep Module** encodes categorical variables (Yes/No → 1/0, etc.)
4. **Scoring Engine** calculates rule-based scores across 7 pillars
5. **ML Model** (optional) adds ML predictions for lead score and status
6. **Response** is cleaned for JSON serialization and returned to frontend
7. **Frontend** displays results with visualizations and stores in LocalStorage

### Technology Stack

**Backend:**
- Python 3.x
- Flask - Web framework
- Pandas - Data manipulation
- Joblib - ML model loading
- Flask-CORS - Cross-origin support

**Frontend:**
- HTML5
- Tailwind CSS (CDN) - Utility-first CSS framework
- Chart.js (CDN) - Data visualization
- Vanilla JavaScript - No framework dependencies
- Google Fonts (Inter) - Typography

**ML Models:**
- Scikit-learn models (trained separately)
- Lead score regression model
- Lead status classification model

## Scoring System

### Rule-Based Scoring

The scoring engine (`src/scoring_engine.py`) implements a 100-point scoring system:

#### Google Presence (20 points)
- Rating tier: ≥4.5 (10pts), ≥4.0 (8pts), ≥3.5 (5pts), ≥3.0 (3pts), <3.0 (0pts)
- Review count tier: ≥200 (10pts), ≥100 (8pts), ≥50 (5pts), ≥20 (3pts), <20 (0pts)

#### Instagram Activity (20 points)
- Active account: 10 points
- Follower tier: ≥5000 (10pts), ≥2000 (8pts), ≥500 (5pts), ≥100 (3pts), <100 (0pts)

#### Website Status (15 points)
- Good: 15 points
- Basic: 8 points
- None: 0 points

#### WhatsApp Availability (15 points)
- Available: 15 points
- Not available: 0 points

#### Menu/Catalog (10 points)
- Available: 10 points
- Not available: 0 points

#### Branding Quality (10 points)
- High: 10 points
- Medium: 6 points
- Low: 2 points
- Not set: 0 points

#### Online Ordering (10 points)
- Available: 10 points
- Not available: 0 points

### Weakness Detection

A pillar is considered a weakness if its score is below 50% of its maximum points. Weaknesses are mapped to B Socio services:

- Google Presence → Google Business Profile Optimization
- Instagram Activity → Instagram Growth & Content Strategy
- Website Status → Website Development & Optimization
- WhatsApp Availability → WhatsApp Business Setup & Automation
- Menu/Catalog → Digital Menu/Catalog Creation
- Branding Quality → Brand Identity & Visual Design
- Online Ordering → E-commerce & Online Ordering System

### Personalized DM Generation

The system generates personalized outreach messages based on the business's biggest weakness:

```
Hi {Business Name}!

I noticed your {Pillar Name} could use some improvement (currently at {Score}/{Max}). 
At B Socio, we specialize in {Service} to help businesses like yours stand out online.

Would you be open to a quick chat about how we can help?
```

### ML Predictions (Optional)

When ML models are available, the system adds:
- **ml_lead_score**: ML-predicted lead score (regression)
- **ml_lead_status**: ML-predicted lead status (classification)

These complement the rule-based scores and provide an additional perspective.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to the project root:
```bash
cd B-Socio-Lead-Scoring
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install web backend dependencies:
```bash
pip install -r web/backend/requirements.txt
```

### Frontend Setup

The frontend uses CDN-hosted libraries, so no installation is required. Simply serve the HTML files using any static file server.

### ML Models (Optional)

If you have trained ML models, place them in the `models/` directory:
- `lead_score_model.pkl`
- `lead_status_classifier.pkl`

If models are not available, the system will still function using rule-based scoring only.

## Running the Application

### Quick Start (Windows)

```bash
start.bat
```

This script will start both the backend and frontend servers.

### Manual Start

#### Start Flask Backend

```bash
cd web/backend
python app.py
```

The Flask server will start on `http://localhost:5000`

#### Serve Frontend

Choose one of the following options:

**Option 1: Python's built-in server**
```bash
cd web/frontend
python -m http.server 8080
```

**Option 2: Node.js http-server**
```bash
cd web/frontend
npx http-server -p 8080
```

**Option 3: VS Code Live Server**
- Install the "Live Server" extension
- Right-click on `index.html` → "Open with Live Server"

The frontend will be available at `http://localhost:8080`

### Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:5000`

## API Documentation

### POST /api/score-csv

Upload a CSV file to score businesses.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` field containing CSV file

**CSV Format Requirements:**
The CSV must include the following columns:
- business_name
- phone_available (Yes/No)
- whatsapp_available (Yes/No)
- instagram_active (Yes/No)
- instagram_followers (number)
- facebook_active (Yes/No)
- website_status (None/Basic/Good)
- google_rating (0-5)
- google_reviews_count (number)
- menu_catalog_available (Yes/No)
- branding_quality (Low/Medium/High)
- years_in_business (number)
- online_orders_accepted (Yes/No)
- category (optional)
- location (optional)

**Response:**
```json
{
  "success": true,
  "count": 20,
  "businesses": [
    {
      "business_name": "Example Business",
      "total_score": 75,
      "status": "Hot",
      "score_google_presence": 15,
      "score_instagram_activity": 18,
      "score_website_status": 15,
      "score_whatsapp_availability": 15,
      "score_menu_catalog": 10,
      "score_branding_quality": 6,
      "score_online_ordering": 10,
      "ml_lead_score": 78.5,
      "ml_lead_status": "Hot"
    }
  ]
}
```

**Error Response:**
```json
{
  "error": "File must be a CSV"
}
```

### POST /api/score-manual

Score a single business from JSON data.

**Request:**
- Method: POST
- Content-Type: application/json
- Body: JSON object with business fields

**Request Body:**
```json
{
  "business_name": "Example Business",
  "category": "Restaurant",
  "location": "Ludhiana",
  "phone_available": "Yes",
  "whatsapp_available": "Yes",
  "instagram_active": "Yes",
  "instagram_followers": 2500,
  "facebook_active": "Yes",
  "website_status": "Good",
  "google_rating": 4.5,
  "google_reviews_count": 150,
  "menu_catalog_available": "Yes",
  "branding_quality": "High",
  "years_in_business": 5,
  "online_orders_accepted": "Yes"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "business_name": "Example Business",
    "total_score": 75,
    "status": "Hot",
    "pillar_scores": {
      "google_presence": 18,
      "instagram_activity": 18,
      "website_status": 15,
      "whatsapp_availability": 15,
      "menu_catalog": 10,
      "branding_quality": 10,
      "online_ordering": 10,
      "total_score": 96
    },
    "weaknesses": [],
    "personalized_dm": null
  }
}
```

### GET /api/sample-data

Get sample business data as JSON for testing.

**Response:**
```json
{
  "success": true,
  "count": 20,
  "businesses": [...]
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Frontend Pages

### Index (Landing Page)

**Purpose:** Introduction to the B Socio Lead Scoring system

**Features:**
- Hero section with gradient background
- Feature highlights
- Call-to-action buttons
- Responsive design

**Navigation:** Links to Upload and Manual Entry pages

### Upload (CSV Upload)

**Purpose:** Bulk scoring of businesses from CSV files

**Features:**
- Drag-and-drop file upload zone
- File validation (CSV only)
- Loading state during processing
- Results table with sortable columns
- Business detail modal on click
- Download scored CSV functionality
- LocalStorage persistence (data persists across page navigation)

**Data Flow:**
1. User uploads CSV
2. File is sent to `/api/score-csv`
3. Results are displayed in table
4. Data is stored in LocalStorage
5. Dashboard can access this data

### Manual Entry

**Purpose:** Single business scoring with live preview

**Features:**
- 15-field form with validation
- Live score preview (updates as you type)
- Progress indicator showing fields completed
- Pillar score breakdown in real-time
- Weakness detection as you fill the form
- Service pitch recommendation
- Debounced API calls (400ms) for performance
- Results panel with detailed breakdown
- Personalized DM generation
- Reset form functionality
- LocalStorage persistence (adds to existing data)

**Live Preview:**
- Shows estimated score before submission
- Displays pillar scores with progress bars
- Highlights weaknesses as they're detected
- Recommends service to pitch based on biggest weakness

### Dashboard

**Purpose:** Analytics and insights from scored businesses

**Features:**
- Stat cards (Total Businesses, Hot/Warm/Cold leads)
- Clickable stat cards to view filtered lists
- Lead Status Distribution (doughnut chart)
- Average Score by Category (bar chart)
- Most Common Weaknesses (horizontal bar chart)
- Modal system for detailed business views
- Defaults to 0 (no data) until data is loaded from Upload/Manual Entry

**Data Source:**
- Loads from LocalStorage (populated by Upload/Manual Entry pages)
- Does not auto-load on page load (user must first score data)

## Data Flow

### CSV Upload Flow

```
User uploads CSV → Frontend validates → POST /api/score-csv → 
Backend processes → Data prep → Rule-based scoring → ML predictions → 
JSON response → Frontend displays → Store in LocalStorage → Dashboard access
```

### Manual Entry Flow

```
User fills form → Live preview (debounced) → User submits → 
POST /api/score-manual → Backend processes → Data prep → 
Rule-based scoring → JSON response → Frontend displays → 
Add to LocalStorage → Dashboard access
```

### Dashboard Flow

```
User navigates to Dashboard → Check LocalStorage → 
If data exists → Display charts and stats → 
If no data → Show empty state (0s)
```

## Performance Optimizations

### Frontend Optimizations

1. **Event Listener Optimization**
   - Removed redundant 'change' event listeners (only 'input' needed)
   - Reduced unnecessary function calls

2. **CSS Transition Optimization**
   - Changed from `transition: all 0.3s` to specific properties
   - Reduced duration from 0.3s to 0.2s
   - Added `will-change` hints for GPU acceleration
   - Applied to: buttons, cards, form inputs

3. **Chart Animation Optimization**
   - Added 500ms duration with `easeOutQuart` easing
   - Applied to all Chart.js instances (status, category, weaknesses charts)
   - Smoother animations without excessive duration

4. **Scroll Event Throttling**
   - Added 16ms (~60fps) throttling to scroll event listeners
   - Prevents excessive DOM updates during scroll
   - Applied across all pages (index, upload, manual-entry, dashboard, navbar)

5. **API Call Debouncing**
   - 400ms debounce on live preview API calls
   - Prevents excessive API requests during form input
   - Improves performance and reduces server load

6. **LocalStorage Persistence**
   - Data persists across page navigation without refresh
   - Reduces need for re-scoring or re-uploading

### Backend Optimizations

1. **Efficient Data Processing**
   - Pandas for fast data manipulation
   - Vectorized operations where possible

2. **Graceful ML Fallback**
   - ML predictions are optional
   - System functions with rule-based scoring only if models unavailable

3. **JSON Serialization**
   - Utility functions to handle NaN values
   - Prevents serialization errors

## Testing

### Backend Testing

```bash
# Health check
curl http://localhost:5000/health

# Get sample data
curl http://localhost:5000/api/sample-data

# Test CSV scoring
curl -X POST -F "file=@test.csv" http://localhost:5000/api/score-csv

# Test manual scoring
curl -X POST -H "Content-Type: application/json" \
  -d '{"business_name":"Test","phone_available":"Yes",...}' \
  http://localhost:5000/api/score-manual
```

### Frontend Testing

1. **Functional Testing**
   - Open `http://localhost:8080`
   - Navigate through all pages
   - Test CSV upload with sample data
   - Test manual entry form
   - Verify live preview updates
   - Check dashboard displays data correctly
   - Test download functionality

2. **Responsive Testing**
   - Test at mobile viewport (375px)
   - Test at tablet viewport (768px)
   - Test at desktop viewport (1440px)
   - Verify hamburger menu works on mobile

3. **Cross-Browser Testing**
   - Chrome/Edge (Chromium)
   - Firefox
   - Safari

4. **Performance Testing**
   - Monitor scroll smoothness
   - Check form input responsiveness
   - Verify chart animations are smooth
   - Test with large CSV files (100+ businesses)

## Deployment

### Vercel Deployment

The application is configured for Vercel deployment:

1. **Backend Deployment**
   - Vercel automatically detects Python
   - Uses `web/backend/app.py` as entry point
   - Environment variables configured in Vercel dashboard

2. **Frontend Deployment**
   - Static files served from `web/frontend/`
   - No build step required
   - CDN libraries loaded at runtime

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
FRONTEND_URL=https://your-frontend-url.vercel.app
```

### Local Production

For local production deployment:

1. Use a production WSGI server (Gunicorn):
```bash
pip install gunicorn
cd web/backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Use a production static file server (nginx) for frontend
3. Configure reverse proxy to route API requests to backend

## Troubleshooting

### Common Issues

**Issue: CORS errors when accessing API**
- Solution: Ensure Flask-CORS is installed and enabled in app.py

**Issue: ML predictions not appearing**
- Solution: Check that model files exist in `models/` directory
- ML predictions are optional - system works with rule-based scoring only

**Issue: CSV upload fails**
- Solution: Verify CSV format matches required columns
- Check that file is properly encoded (UTF-8)

**Issue: Dashboard shows 0s after scoring**
- Solution: This is expected behavior - dashboard defaults to 0
- Data only appears after you score via Upload or Manual Entry pages

**Issue: Live preview not updating**
- Solution: Check browser console for errors
- Verify backend is running on port 5000
- Check that API_BASE is correctly set in manual-entry.html

**Issue: Scroll performance is laggy**
- Solution: Ensure scroll throttling is implemented
- Check for excessive console logging
- Verify CSS transitions are optimized

**Issue: Charts not rendering**
- Solution: Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify canvas elements exist in DOM

### Debug Mode

Enable Flask debug mode for detailed error messages:

```python
# In web/backend/app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Logs

Check backend console for:
- API request logs
- Error messages
- ML model loading status

Check browser console for:
- Frontend errors
- Network request failures
- JavaScript errors

## Contributing

When contributing to this project:

1. Follow the existing code style
2. Add comments for complex logic
3. Test both frontend and backend changes
4. Update documentation as needed
5. Ensure performance optimizations are maintained

## License

This project is proprietary to B Socio.

## Support

For issues or questions:
- Check the Troubleshooting section
- Review API documentation
- Check browser and server console logs
