# B Socio AI Lead Scoring System

A comprehensive AI-powered lead scoring system that evaluates businesses based on their digital presence across multiple platforms. This system helps sales teams identify high-potential leads by analyzing 7 key digital pillars and providing actionable insights.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-Proprietary-red)

## 🎯 Overview

B Socio Lead Scoring transforms how businesses evaluate potential leads by combining rule-based scoring with machine learning predictions. The system analyzes a business's digital footprint across Google, Instagram, Website, WhatsApp, and other platforms to generate a comprehensive lead score (0-100) and classify leads as Hot, Warm, or Cold.

### Key Features

- **Multi-Pillar Scoring**: Evaluates businesses across 7 digital presence pillars
- **Rule-Based Engine**: Transparent scoring logic with clear point distribution
- **ML Predictions**: Optional machine learning models for enhanced accuracy
- **Live Preview**: Real-time score estimation during manual entry
- **Bulk Processing**: CSV upload for scoring hundreds of businesses at once
- **Analytics Dashboard**: Interactive charts and visualizations
- **Personalized Outreach**: Auto-generated DMs based on detected weaknesses
- **Service Recommendations**: Maps weaknesses to specific B Socio services

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │  Scoring Engine │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│  (Rule-Based)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  ML Models    │
                                              │  (Optional)   │
                                              └───────────────┘
```

### Technology Stack

**Backend:**
- **Flask** - REST API server
- **Pandas** - Data manipulation and processing
- **Scikit-learn** - Machine learning model loading
- **Joblib** - Model serialization

**Frontend:**
- **HTML5** - Markup
- **Tailwind CSS** - Styling (via CDN)
- **Chart.js** - Data visualization (via CDN)
- **Vanilla JavaScript** - No framework dependencies

**ML Models:**
- **Random Forest Regressor** - Lead score prediction
- **Random Forest Classifier** - Lead status classification

## 📊 Scoring System

### The 7 Digital Pillars

The scoring system evaluates businesses across 7 pillars, totaling 100 points:

| Pillar | Max Points | Scoring Criteria |
|--------|------------|-----------------|
| **Google Presence** | 20 | Google rating (0-10) + Review count tier (0-10) |
| **Instagram Activity** | 20 | Active account (10) + Follower tier (0-10) |
| **Website Status** | 15 | Good (15), Basic (8), None (0) |
| **WhatsApp Availability** | 15 | Available (15), Not available (0) |
| **Menu/Catalog** | 10 | Available (10), Not available (0) |
| **Branding Quality** | 10 | High (10), Medium (6), Low (2), Not set (0) |
| **Online Ordering** | 10 | Available (10), Not available (0) |

### Lead Classification

Based on the total score (0-100):

- 🔥 **Hot Lead (75-100)**: High potential, ready for immediate outreach
- 🌡️ **Warm Lead (45-74)**: Moderate potential, needs nurturing
- ❄️ **Cold Lead (0-44)**: Low potential, requires significant improvement

### Detailed Scoring Logic

#### Google Presence (20 points)
- **Rating Tier:**
  - ≥4.5 → 10 points
  - ≥4.0 → 8 points
  - ≥3.5 → 5 points
  - ≥3.0 → 3 points
  - <3.0 → 0 points
- **Review Count Tier:**
  - ≥200 → 10 points
  - ≥100 → 8 points
  - ≥50 → 5 points
  - ≥20 → 3 points
  - <20 → 0 points

#### Instagram Activity (20 points)
- **Active Account:** 10 points (Yes/No)
- **Follower Tier:**
  - ≥5000 → 10 points
  - ≥2000 → 8 points
  - ≥500 → 5 points
  - ≥100 → 3 points
  - <100 → 0 points

#### Website Status (15 points)
- Good → 15 points
- Basic → 8 points
- None → 0 points

#### WhatsApp Availability (15 points)
- Available → 15 points
- Not available → 0 points

#### Menu/Catalog (10 points)
- Available → 10 points
- Not available → 0 points

#### Branding Quality (10 points)
- High → 10 points
- Medium → 6 points
- Low → 2 points
- Not set → 0 points

#### Online Ordering (10 points)
- Available → 10 points
- Not available → 0 points

### Weakness Detection

A pillar is flagged as a weakness if its score is below 50% of its maximum points. Each weakness is mapped to a specific B Socio service:

| Weakness | Recommended Service |
|----------|-------------------|
| Google Presence | Google Business Profile Optimization |
| Instagram Activity | Instagram Growth & Content Strategy |
| Website Status | Website Development & Optimization |
| WhatsApp Availability | WhatsApp Business Setup & Automation |
| Menu/Catalog | Digital Menu/Catalog Creation |
| Branding Quality | Brand Identity & Visual Design |
| Online Ordering | E-commerce & Online Ordering System |

### Personalized DM Generation

The system automatically generates personalized outreach messages based on the biggest weakness:

```
Hi {Business Name}!

I noticed your {Pillar Name} could use some improvement 
(currently at {Score}/{Max}). At B Socio, we specialize in 
{Service} to help businesses like yours stand out online.

Would you be open to a quick chat about how we can help?
```

## 🤖 Machine Learning Models

### Model Overview

The system includes optional ML models that complement the rule-based scoring:

1. **Lead Score Regression Model** (`lead_score_model.pkl`)
   - Predicts a numerical lead score (0-100)
   - Trained on historical business data
   - Uses Random Forest algorithm

2. **Lead Status Classifier** (`lead_status_classifier.pkl`)
   - Predicts lead status (Hot/Warm/Cold)
   - Trained on historical business data
   - Uses Random Forest algorithm

### Model Features

The models use the following features for prediction:
- whatsapp_available
- instagram_active
- instagram_followers
- facebook_active
- website_status_score
- google_rating
- google_reviews_count
- menu_catalog_available
- branding_quality_score
- years_in_business
- online_orders_accepted

### Graceful Degradation

ML predictions are optional. If models are not available, the system functions perfectly with rule-based scoring only. This ensures reliability regardless of ML model availability.

## 🎨 Frontend

### Pages

#### 1. Landing Page (`index.html`)
- Modern hero section with gradient background
- Feature highlights
- Call-to-action buttons
- Responsive design

#### 2. CSV Upload (`upload.html`)
- Drag-and-drop file upload zone
- File validation (CSV only)
- Real-time processing with loading states
- Results table with sortable columns
- Business detail modal on click
- Download scored CSV functionality
- LocalStorage persistence

#### 3. Manual Entry (`manual-entry.html`)
- 15-field form with validation
- **Live score preview** (updates as you type)
- Progress indicator showing fields completed
- Pillar score breakdown in real-time
- Weakness detection as you fill the form
- Service pitch recommendation
- Debounced API calls (400ms) for performance
- Results panel with detailed breakdown
- Personalized DM generation
- Reset form functionality

#### 4. Dashboard (`dashboard.html`)
- Stat cards (Total Businesses, Hot/Warm/Cold leads)
- Clickable stat cards to view filtered lists
- **Lead Status Distribution** (doughnut chart)
- **Average Score by Category** (bar chart)
- **Most Common Weaknesses** (horizontal bar chart)
- Modal system for detailed business views

### Frontend Features

- **Responsive Design**: Mobile-first approach with breakpoints at 375px, 768px, 1440px
- **LocalStorage Persistence**: Data persists across page navigation
- **Performance Optimizations**:
  - Debounced API calls (400ms)
  - Throttled scroll events (16ms)
  - GPU-accelerated CSS transitions
  - Optimized Chart.js animations (500ms)
- **Loading States**: Spinners during API calls
- **Error Handling**: Friendly error messages
- **Modal System**: For detailed business views

## 🔧 Backend

### API Endpoints

#### POST `/api/score-csv`
Upload a CSV file to score businesses in bulk.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` field containing CSV file

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
      "ml_lead_score": 78.5,
      "ml_lead_status": "Hot"
    }
  ]
}
```

#### POST `/api/score-manual`
Score a single business from JSON data.

**Request:**
- Method: POST
- Content-Type: application/json
- Body: JSON object with business fields

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

#### GET `/api/sample-data`
Get sample business data for testing.

**Response:**
```json
{
  "success": true,
  "count": 20,
  "businesses": [...]
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### Backend Features

- **CORS Enabled**: Cross-origin support for frontend communication
- **Data Preparation**: Automatic encoding of categorical variables
- **Rule-Based Scoring**: Transparent scoring logic
- **ML Integration**: Optional ML predictions
- **Error Handling**: Comprehensive error logging
- **JSON Serialization**: Utilities for handling NaN values

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rajdeeplotey/Lead-Scoring.git
cd B-Socio-Lead-Scoring
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r web/backend/requirements.txt
```

3. **Place ML models (optional)**
```bash
# Place your trained models in the models/ directory:
# - lead_score_model.pkl
# - lead_status_classifier.pkl
```

### Running the Application

#### Quick Start (Windows)
```bash
start.bat
```

#### Manual Start

**Start Backend:**
```bash
cd web/backend
python app.py
```
Backend runs on `http://localhost:5000`

**Start Frontend:**
```bash
cd web/frontend
python -m http.server 8080
```
Frontend runs on `http://localhost:8080`

### Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:5000`

## 📁 Project Structure

```
B-Socio-Lead-Scoring/
├── data/                          # Sample data files
├── models/                        # ML model files
├── src/                           # Core scoring logic
│   ├── data_prep.py               # Data preparation
│   ├── scoring_engine.py         # Rule-based scoring
│   └── ml_model.py                # ML model wrapper
├── web/                           # Web application
│   ├── backend/
│   │   ├── app.py                 # Flask API
│   │   └── utils.py               # Utilities
│   └── frontend/
│       ├── index.html             # Landing page
│       ├── upload.html            # CSV upload
│       ├── manual-entry.html      # Manual entry
│       ├── dashboard.html         # Analytics
│       └── styles.css             # Custom styles
└── requirements.txt
```

## 🧪 Testing

### Backend Testing
```bash
# Health check
curl http://localhost:5000/health

# Get sample data
curl http://localhost:5000/api/sample-data

# Test CSV scoring
curl -X POST -F "file=@test.csv" http://localhost:5000/api/score-csv
```

### Frontend Testing
1. Open `http://localhost:8080`
2. Navigate through all pages
3. Test CSV upload with sample data
4. Test manual entry form
5. Verify live preview updates
6. Check dashboard displays data correctly

## 📊 CSV Format

The CSV file must include the following columns:

**Required Columns:**
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

**Optional Columns:**
- category
- location

## 🔒 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
FRONTEND_URL=https://your-frontend-url.vercel.app
```

## 🚢 Deployment

### Vercel Deployment

The application is configured for Vercel deployment:

1. **Backend**: Vercel automatically detects Python and uses `web/backend/app.py`
2. **Frontend**: Static files served from `web/frontend/`
3. **Environment Variables**: Configure in Vercel dashboard

### Local Production

For local production deployment:

1. Use Gunicorn for backend:
```bash
pip install gunicorn
cd web/backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Use nginx for frontend static files
3. Configure reverse proxy for API routing

## 🐛 Troubleshooting

**Issue: CORS errors**
- Ensure Flask-CORS is installed and enabled

**Issue: ML predictions not appearing**
- Check that model files exist in `models/` directory
- ML predictions are optional - system works without them

**Issue: CSV upload fails**
- Verify CSV format matches required columns
- Check file encoding (UTF-8)

**Issue: Dashboard shows 0s**
- This is expected - dashboard defaults to 0
- Score data via Upload or Manual Entry first

**Issue: Live preview not updating**
- Check browser console for errors
- Verify backend is running on port 5000

## 📝 License

This project is proprietary to B Socio.

## 🤝 Contributing

When contributing:
1. Follow existing code style
2. Add comments for complex logic
3. Test both frontend and backend changes
4. Update documentation as needed
5. Maintain performance optimizations

## 📧 Support

For issues or questions:
- Check the Troubleshooting section
- Review API documentation
- Check browser and server console logs

---

**Built with ❤️ by B Socio**
