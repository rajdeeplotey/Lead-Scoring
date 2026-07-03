# 📊 B Socio — AI Lead Scoring System

An AI-powered lead scoring system that evaluates local businesses based on their **digital presence** (Google, Instagram, website, WhatsApp, and more) and turns that into a clear 0–100 lead score, a Hot/Warm/Cold classification, and a ready-to-send personalized outreach message.

Built for sales/growth teams (originally for **B Socio**, a digital marketing agency in Ludhiana/Khanna) who need to quickly figure out *which* businesses are worth pitching, and *what* to pitch them.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Alt%20UI-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Models-orange)
![License](https://img.shields.io/badge/License-Proprietary-lightgrey)

---

## Table of Contents

- [Overview](#overview)
- [How Scoring Works](#how-scoring-works)
- [Machine Learning Layer](#machine-learning-layer)
- [Project Structure](#project-structure)
- [Two Ways to Run It](#two-ways-to-run-it)
- [Installation](#installation)
- [Running the Web App (Flask + HTML)](#running-the-web-app-flask--html)
- [Running the Streamlit App](#running-the-streamlit-app)
- [API Reference](#api-reference)
- [CSV Data Format](#csv-data-format)
- [Environment Variables](#environment-variables)
- [Deployment (Vercel)](#deployment-vercel)
- [Retraining the ML Models](#retraining-the-ml-models)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

Instead of manually stalking a business's Instagram and Google listing to guess whether they'd want your services, this tool does it systematically. Feed it business data (one at a time, or a whole CSV of leads) and it will:

1. Score the business out of **100 points** across **7 digital-presence pillars**.
2. Classify it as a **🔥 Hot**, **🌡️ Warm**, or **❄️ Cold** lead.
3. Detect the business's biggest **weaknesses** (e.g. no WhatsApp, weak Instagram).
4. Map each weakness to a **specific service** B Socio could pitch.
5. Auto-draft a **personalized outreach DM** targeting the biggest weakness.
6. Optionally cross-check the rule-based score with a **machine learning prediction**.

There are two interfaces to the same scoring engine:

| Interface | Stack | Best for |
|---|---|---|
| **Web App** | Flask API + static HTML/Tailwind/Chart.js frontend | Production use, CSV bulk uploads, dashboards, deployment |
| **Streamlit App** | Single-file Streamlit app (`src/app.py`) | Quick local demos / internal tooling, no separate frontend needed |

Both call the exact same core logic in `src/` (`data_prep.py`, `scoring_engine.py`, `ml_model.py`), so scores are always consistent regardless of which UI you use.

---

## How Scoring Works

The scoring engine (`src/scoring_engine.py`) is fully transparent, rule-based, and adds up to 100 points across 7 pillars:

| Pillar | Max Points | Criteria |
|---|---|---|
| **Google Presence** | 20 | Rating tier (0–10) + review-count tier (0–10) |
| **Instagram Activity** | 20 | Active account (10) + follower tier (0–10) |
| **Website Status** | 15 | Good = 15, Basic = 8, None = 0 |
| **WhatsApp Availability** | 15 | Available = 15, Not available = 0 |
| **Menu / Catalog** | 10 | Available = 10, Not available = 0 |
| **Branding Quality** | 10 | High = 10, Medium = 6, Low = 2, Not set = 0 |
| **Online Ordering** | 10 | Available = 10, Not available = 0 |

### Tier breakdowns

**Google rating**
`≥4.5 → 10` · `≥4.0 → 8` · `≥3.5 → 5` · `≥3.0 → 3` · `<3.0 → 0`

**Google review count**
`≥200 → 10` · `≥100 → 8` · `≥50 → 5` · `≥20 → 3` · `<20 → 0`

**Instagram followers**
`≥5000 → 10` · `≥2000 → 8` · `≥500 → 5` · `≥100 → 3` · `<100 → 0`

### Lead classification

- 🔥 **Hot** — 75 to 100 → ready for immediate outreach
- 🌡️ **Warm** — 45 to 74 → needs nurturing
- ❄️ **Cold** — 0 to 44 → needs significant digital improvement first

### Weakness detection & service mapping

A pillar is flagged as a **weakness** whenever it scores below **50% of its maximum**. Each weakness maps directly to a B Socio service to pitch:

| Weak Pillar | Recommended Service |
|---|---|
| Google Presence | Google Business Profile Optimization |
| Instagram Activity | Instagram Growth & Content Strategy |
| Website Status | Website Development & Optimization |
| WhatsApp Availability | WhatsApp Business Setup & Automation |
| Menu / Catalog | Digital Menu/Catalog Creation |
| Branding Quality | Brand Identity & Visual Design |
| Online Ordering | E-commerce & Online Ordering System |

### Personalized DM generation

The system picks the business's single **biggest weakness** (largest points-missing gap) and drafts a ready-to-send message:

```
Hi {Business Name}!

I noticed your {Pillar Name} could use some improvement
(currently at {Score}/{Max}). At B Socio, we specialize in
{Service} to help businesses like yours stand out online.

Would you be open to a quick chat about how we can help?
```

---

## Machine Learning Layer

On top of the transparent rule-based engine, the system can optionally load two pre-trained **scikit-learn Random Forest** models (`models/lead_score_model.pkl` and `models/lead_status_classifier.pkl`):

- **Lead Score Regressor** → predicts a numeric score (0–100)
- **Lead Status Classifier** → predicts Hot / Warm / Cold directly

Both models are trained on these features: `whatsapp_available`, `instagram_active`, `instagram_followers`, `facebook_active`, `website_status_score`, `google_rating`, `google_reviews_count`, `menu_catalog_available`, `branding_quality_score`, `years_in_business`, `online_orders_accepted`.

**Important Disclosure**: The training labels (lead score and Hot/Warm/Cold status) were **generated by the rule-based scoring engine itself**, not from real conversion or sales outcome data. This is a prototype/proof-of-concept limitation — the ML models learn to replicate the rule-based logic, not predict actual business conversions. The metrics in `MODEL_EVALUATION.md` reflect how well the ML learned the rules, not real-world predictive performance.

**ML is fully optional.** If the `.pkl` files are missing or fail to load, `src/ml_model.py` fails gracefully and the app keeps working on rule-based scoring alone — no crashes, just a console warning.

---

## Project Structure

```
B-Socio-Lead-Scoring/
├── data/
│   ├── ludhiana_training_data_150.csv     # Training data for the ML models
│   └── sample_businesses_khanna.csv       # Sample data used by "/api/sample-data"
├── models/
│   ├── lead_score_model.pkl               # Trained regressor (optional)
│   └── lead_status_classifier.pkl         # Trained classifier (optional)
├── notebooks/
│   └── model_training.ipynb               # Notebook used to train the ML models
├── src/                                    # Core scoring logic (shared by both UIs)
│   ├── app.py                              # Streamlit app (Upload CSV + Manual Entry tabs)
│   ├── data_prep.py                        # CSV loading & categorical encoding
│   ├── scoring_engine.py                   # Rule-based 100-point scoring engine
│   └── ml_model.py                         # Loads .pkl models & adds ML predictions
├── web/
│   ├── backend/
│   │   ├── app.py                          # Flask REST API (imports from src/)
│   │   ├── utils.py                        # JSON-serialization helpers (NaN handling)
│   │   └── requirements.txt
│   └── frontend/
│       ├── index.html                      # Landing page
│       ├── upload.html                     # Bulk CSV upload + results table
│       ├── manual-entry.html               # Single-lead form with live score preview
│       ├── dashboard.html                  # Chart.js analytics dashboard
│       ├── navbar.html / footer.html       # Shared components
│       └── styles.css
├── instance/bsocio.db                      # SQLite DB (Flask default instance folder)
├── .env                                    # Environment variables (see below)
├── pyproject.toml                          # Vercel entrypoint + dependency list
├── requirements.txt                        # Root Python dependencies
├── start.bat                               # One-click Windows launcher (backend + frontend)
└── README.md
```

---

## Two Ways to Run It

Pick whichever interface fits your workflow — both share the same scoring engine.

1. **Web App** (recommended for real use, dashboards, deployment) — Flask API + static HTML frontend.
2. **Streamlit App** (recommended for quick local testing/demo) — a single command spins up an interactive UI with an Upload CSV tab and a Manual Entry tab.

---

## Installation

**Prerequisites:** Python 3.9+ and pip.

```bash
git clone https://github.com/rajdeeplotey/Lead-Scoring.git
cd B-Socio-Lead-Scoring

# Core dependencies
pip install -r requirements.txt

# Backend-specific dependencies (same list, kept separate for Vercel)
pip install -r web/backend/requirements.txt

# Only needed if you want to run the Streamlit interface
pip install streamlit
```

ML models are optional — if you have trained `.pkl` files, drop them into `models/`:

```
models/lead_score_model.pkl
models/lead_status_classifier.pkl
```

---

## Running the Web App (Flask + HTML)

### Quick start (Windows)

```bash
start.bat
```

This launches the Flask backend on port 5000 and a static file server for the frontend on port 8080, then opens your browser automatically.

### Manual start (any OS)

**Backend:**
```bash
cd web/backend
python app.py
```
Runs on `http://localhost:5000`

**Frontend** (in a second terminal):
```bash
cd web/frontend
python -m http.server 8080
```
Runs on `http://localhost:8080`

Then open `http://localhost:8080` in your browser. The frontend talks to the Flask API for scoring, and persists results in browser LocalStorage so the Dashboard page can chart them.

### Frontend pages

- **`index.html`** — Landing page with hero section and CTAs to Upload/Manual Entry.
- **`upload.html`** — Drag-and-drop CSV upload, results table, per-business detail modal, and a "download scored CSV" button.
- **`manual-entry.html`** — 15-field form with a **live score preview** (debounced ~400ms API calls) that updates pillar scores and weaknesses as you type.
- **`dashboard.html`** — Chart.js visualizations: lead status distribution (doughnut), average score by category (bar), and most common weaknesses (horizontal bar). Populated from whatever's in LocalStorage.

---

## Running the Streamlit App

```bash
pip install streamlit
streamlit run src/app.py
```

This opens a local Streamlit app with two tabs:

- **Upload CSV** — upload a business CSV, see a color-coded scored table (Hot/Warm/Cold), download the scored CSV, and drill into any single business for a full score card + weaknesses + DM.
- **Manual Entry** — fill out a form for one business and get an instant score card with pillar progress bars and a personalized DM.

---

## API Reference

Base URL when running locally: `http://localhost:5000`

### `POST /api/score-csv`
Score every business in an uploaded CSV.

- **Content-Type:** `multipart/form-data`
- **Body:** `file` — a `.csv` file (see [CSV format](#csv-data-format))

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

### `POST /api/score-manual`
Score a single business from JSON.

- **Content-Type:** `application/json`
- **Body:** business fields (see [CSV format](#csv-data-format) — same field names)

```json
{
  "success": true,
  "result": {
    "business_name": "Example Business",
    "total_score": 96,
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

### `GET /api/sample-data`
Returns the bundled sample dataset (`data/sample_businesses_khanna.csv`) as JSON — handy for testing the frontend without your own file.

### `GET /health`
Simple health check — returns `{"status": "healthy"}`.

---

## CSV Data Format

For both `/api/score-csv` and the Streamlit Upload tab, your CSV needs these columns:

**Required:**
| Column | Type / Values |
|---|---|
| `business_name` | text |
| `phone_available` | `Yes` / `No` |
| `whatsapp_available` | `Yes` / `No` |
| `instagram_active` | `Yes` / `No` |
| `instagram_followers` | number |
| `facebook_active` | `Yes` / `No` |
| `website_status` | `None` / `Basic` / `Good` |
| `google_rating` | number, 0–5 |
| `google_reviews_count` | number |
| `menu_catalog_available` | `Yes` / `No` |
| `branding_quality` | `Low` / `Medium` / `High` |
| `years_in_business` | number |
| `online_orders_accepted` | `Yes` / `No` |

**Optional:** `category`, `location`

A ready-to-use example lives at `data/sample_businesses_khanna.csv`.

---

## Environment Variables

Create a `.env` file in the project root (an example already exists — replace the placeholder values before deploying):

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///bsocio.db
FRONTEND_URL=https://your-frontend-url.vercel.app

# Optional — only needed if the app sends email (e.g. verification links)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

> ⚠️ **Never commit real secrets.** Make sure `.env` is in `.gitignore` before pushing to GitHub, and rotate any credentials that may already be exposed.

---

## Deployment (Vercel)

The project is pre-configured for Vercel (`pyproject.toml` sets the entrypoint to `web.backend.app:app`):

1. **Backend** — Vercel detects the Python entrypoint automatically and serves the Flask API.
2. **Frontend** — Flask itself serves the static files in `web/frontend/` (see the `send_from_directory` routes in `web/backend/app.py`), so no separate frontend deployment is needed.
3. **Environment variables** — set `SECRET_KEY` and `FRONTEND_URL` in the Vercel dashboard.

### Local production

```bash
pip install gunicorn
cd web/backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
Put a reverse proxy (e.g. nginx) in front for TLS/static caching if needed.

---

## Retraining the ML Models

The ML models are trained in `notebooks/model_training.ipynb` using `data/ludhiana_training_data_150.csv`. To retrain:

1. Open the notebook: `jupyter notebook notebooks/model_training.ipynb`
2. Update or expand the training CSV with more labeled examples.
3. Re-run the notebook — it fits a `RandomForestRegressor` (lead score) and a `RandomForestClassifier` (lead status).
4. Export both with `joblib` into `models/lead_score_model.pkl` and `models/lead_status_classifier.pkl`, overwriting the existing files.
5. Restart the Flask/Streamlit app — `src/ml_model.py` will pick up the new models automatically.

---

## Future Improvements

The current system is designed as a foundation that can evolve with real-world data. Here are planned improvements:

### ML Model Retraining with Real Outcome Data

The most significant improvement will be retraining the ML models on **actual conversion/sales outcome data** instead of rule-generated labels. This would enable:

- **True predictive power**: The ML model could learn patterns that correlate with actual business conversions
- **Discovery of hidden factors**: The model might identify digital presence indicators that manual rules miss
- **Continuous improvement**: As more conversion data is collected, the model can be retrained to improve accuracy
- **Complementary insights**: ML predictions could highlight businesses that score moderately by rules but have high conversion potential (or vice versa)

### Planned Enhancements

1. **Conversion Tracking Integration**
   - Track which scored leads actually convert to customers
   - Record time-to-conversion metrics
   - Capture deal size/value data

2. **Feature Engineering Improvements**
   - Add new digital presence indicators as they become relevant
   - Incorporate industry-specific scoring weights
   - Add geographic/region-based adjustments

3. **Model Architecture Evolution**
   - Experiment with different ML algorithms (Gradient Boosting, Neural Networks)
   - Implement ensemble methods combining multiple models
   - Add confidence intervals to predictions

4. **Real-Time Scoring**
   - Implement streaming data updates from social media APIs
   - Add automated periodic re-scoring of existing leads
   - Build alert system for significant score changes

5. **Advanced Analytics**
   - Lead journey tracking and attribution
   - A/B testing of outreach strategies by lead score
   - ROI analysis of scoring system effectiveness

### Timeline

These improvements depend on collecting sufficient real conversion data. The current hybrid approach provides a solid foundation while this data is being gathered.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| CORS errors in the browser console | Make sure `flask-cors` is installed; the Flask app enables `CORS(app)` by default. |
| ML predictions never appear | This is expected if `models/*.pkl` are missing — ML is optional and the app falls back to rule-based scoring only. |
| CSV upload fails / errors | Double-check your CSV has all [required columns](#csv-data-format) with the exact `Yes`/`No`/`None`/`Basic`/`Good`/`Low`/`Medium`/`High` values, saved as UTF-8. |
| Dashboard shows all zeros | Expected on first load — the dashboard reads from browser LocalStorage, so score some leads via Upload or Manual Entry first. |
| Live preview on Manual Entry doesn't update | Confirm the Flask backend is running on port 5000 and check the browser console for failed requests. |
| `ModuleNotFoundError` for `data_prep` / `scoring_engine` | Run the backend from within `web/backend/` (or use `start.bat`) so the `sys.path` insert in `app.py` can locate `src/`. |

---

## License
Copyright (c) 2026 [Rajdeep Singh]

This project was created as a personal/technical demonstration project.
All rights reserved. This code may be viewed for evaluation purposes
but may not be copied, modified, or redistributed without permission.
