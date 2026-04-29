# 🧪 GlowGuard Pro — Advanced Skincare Intelligence System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)
![Claude AI](https://img.shields.io/badge/Powered_by-Claude_AI-orange.svg)
![Plotly](https://img.shields.io/badge/Charts-Plotly-purple.svg)

**Live Demo:** [Deploy via Streamlit Community Cloud]

---

## 📖 Overview

GlowGuard Pro is a full-featured dermatology-grade skincare intelligence system built on a **Knowledge-Based Expert System** architecture, enhanced with **Claude AI Vision** for real-time skin analysis.

This is not just a compatibility checker — it's a complete skincare companion with 6 major modules.

---

## 🧩 Features

### 1. 👤 Skin Profile Quiz
- Captures skin type, age, climate, concerns, current actives, sensitivity level, and budget
- Generates a **radar chart** of your skin dimensions (hydration, barrier health, sebum, sensitivity, active tolerance)
- Stores your profile in session state for personalized results across all pages

### 2. 🧪 Chemical Interaction Analyzer
- **Bi-directional lookup** with All Active support (e.g. Sunscreen + any active)
- Rich status labels: AMAN / HATI-HATI / JANGAN / WAJIB
- **Plotly bar chart** showing irritation risk, barrier damage risk, pH clash, and efficacy loss
- Full ingredient profile breakdown (pH, strength, category)
- **Interactive heatmap** — visual matrix of all mapped ingredient combinations
- Safe alternative suggestions when a dangerous combination is detected

### 3. 🔄 Skin Cycling Planner
- Generates a personalized **4-night or 6-night skin cycling schedule**
- Adapts retinol strength to experience level (Beginner/Intermediate/Advanced)
- Includes AM routine with step-by-step layering order
- **Progress prediction chart** — expected skin health improvement over 4 weeks
- Colored day cards with specific product recommendations per night

### 4. 💡 Product Recommendations
- Curated database of effective, accessible skincare products with IDR pricing
- Filterable by skin concern and budget
- Each product shows: brand, ingredients list, pH, rating, and personalized "why this works for you" explanation

### 5. 📸 AI Face Scan — Claude Vision
- Upload a selfie → Claude analyzes your visible skin conditions
- Returns: skin type assessment, visible concerns, barrier health, recommended actives, AM/PM starter routine, and ingredients to avoid
- Powered by `claude-opus-4-5` with vision capability
- User provides their own Anthropic API key (privacy-first design)

### 6. 📊 My Dashboard
- Real-time conflict checker across all your current actives
- Visual concern priority chart
- Summary metrics from your skin profile

---

## 🧠 Technical Architecture

```
Knowledge Layer        →  skincare_rules.csv  (35+ ingredient interaction rules)
Application Layer      →  app.py              (Streamlit multi-page app)
Visualization Layer    →  Plotly              (charts, heatmaps, radar, bar)
AI Layer               →  Anthropic Claude    (Vision API for face scan + text advice)
```

**Feature engineering in the dataset:**
- `Ordinal features`: Strength (Low/Medium/Strong), pH (Low/Neutral/Variable)
- `Categorical features`: Kategori (Retinoid/Exfoliant/Barrier/Antioxidant), Interaction Type
- `Target variables`: Status (AMAN/HATI-HATI/JANGAN/WAJIB), Irritation Risk (Low/Medium/High)

This dataset can be used to train a **classification ML model** (Decision Tree, Random Forest, XGBoost) to predict irritation probability for novel combinations not yet in the database.

---

## 🛠️ Local Setup

```bash
git clone https://github.com/yourusername/glowguard-pro.git
cd glowguard-pro
pip install -r requirements.txt
streamlit run app.py
```

For the AI Face Scan feature, you'll need an [Anthropic API key](https://console.anthropic.com).

---

## 🚀 Deploy to Streamlit Community Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py` as main file
4. The Face Scan API key is entered by users at runtime — no secrets needed in deployment

---

## 📁 File Structure

```
glowguard-pro/
├── app.py                  # Main Streamlit application (all 6 pages)
├── skincare_rules.csv      # Knowledge base (ingredient interaction rules)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔮 Roadmap

- [ ] Expand skincare_rules.csv to 100+ ingredient combinations
- [ ] Add ML-powered irritation probability prediction (Random Forest)
- [ ] Product database via external API (Open Beauty Facts / Skincare API)
- [ ] Multi-language support (Bahasa Indonesia + English toggle)
- [ ] Export routine to PDF / share as link
- [ ] Ingredient label scanner (upload product label → extract actives)

---

## 👩‍💻 Author

Built by Aqeela · Data Architecture + Expert System Design  