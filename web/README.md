# B Socio AI Lead Scoring Web Application

A full-stack web application for AI-powered lead scoring with Flask backend and modern HTML/Tailwind CSS frontend.

## Project Structure

```
web/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── index.html          # Landing page
    ├── upload.html         # CSV upload page
    ├── manual-entry.html   # Manual business entry
    ├── dashboard.html      # Analytics dashboard
    └── navbar.html         # Shared navigation component
```

## Features

### Backend (Flask)
- **POST /api/score-csv** - Upload CSV file, score all businesses
- **POST /api/score-manual** - Score single business from JSON
- **GET /api/sample-data** - Get sample business data
- **GET /health** - Health check endpoint
- CORS enabled for frontend communication
- Reuses existing scoring logic from `src/`

### Frontend (HTML/Tailwind/JS)
- **index.html** - Modern landing page with hero section
- **upload.html** - Drag-and-drop CSV upload with results table
- **manual-entry.html** - Form-based single business entry
- **dashboard.html** - Analytics with Chart.js visualizations
- Fully responsive design (mobile-first)
- Shared navbar with mobile hamburger menu
- Clean, modern UI with smooth transitions

## Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd web/backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

The frontend uses CDN-hosted libraries (Tailwind CSS, Chart.js), so no installation is needed. Just serve the HTML files.

## Running the Application

### Start Flask Backend

From the project root:
```bash
cd web/backend
python app.py
```

The Flask server will start on `http://localhost:5000`

### Serve Frontend

You can serve the frontend using any static file server. Here are a few options:

**Option 1: Using Python's built-in server**
```bash
cd web/frontend
python -m http.server 8080
```

**Option 2: Using Node.js http-server**
```bash
cd web/frontend
npx http-server -p 8080
```

**Option 3: Using VS Code Live Server extension**
- Install the "Live Server" extension in VS Code
- Right-click on `index.html` and select "Open with Live Server"

The frontend will be available at `http://localhost:8080`

## API Endpoints

### POST /api/score-csv
Upload a CSV file to score businesses.

**Request:** `multipart/form-data` with `file` field
**Response:** JSON with scored businesses

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
      ...
    }
  ]
}
```

### POST /api/score-manual
Score a single business from JSON data.

**Request:** JSON with business fields
**Response:** JSON with score, status, weaknesses, service, and DM

```json
{
  "success": true,
  "result": {
    "business_name": "Example Business",
    "total_score": 75,
    "status": "Hot",
    "pillar_scores": {...},
    "weaknesses": [...],
    "personalized_dm": "..."
  }
}
```

### GET /api/sample-data
Get sample business data as JSON.

**Response:** JSON with sample businesses

```json
{
  "success": true,
  "count": 20,
  "businesses": [...]
}
```

## Design Features

- **Color Palette:** Indigo/Purple gradient accent with clean white/gray backgrounds
- **Status Badges:** Hot (red), Warm (amber), Cold (blue)
- **Typography:** Inter font family for modern, readable text
- **Responsive:** Mobile-first design with breakpoints at 375px, 768px, 1440px
- **Loading States:** Spinners and skeleton loaders during API calls
- **Error Handling:** Friendly error messages for failed operations
- **Smooth Transitions:** Hover states and subtle animations

## Testing

### Test Backend
```bash
# Health check
curl http://localhost:5000/health

# Get sample data
curl http://localhost:5000/api/sample-data
```

### Test Frontend
1. Open `http://localhost:8080` in your browser
2. Navigate through all pages (Home, Upload, Manual Entry, Dashboard)
3. Test CSV upload functionality
4. Test manual entry form
5. Test dashboard with sample data
6. Test responsive design at different screen sizes

## Notes

- The Flask backend runs on port 5000
- The frontend can run on any port (8080 recommended)
- CORS is enabled to allow frontend-backend communication
- The backend reuses existing scoring logic from the `src/` directory
- ML predictions are optional and will gracefully fail if models are unavailable
