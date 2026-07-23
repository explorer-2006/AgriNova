# AgriNova 

**Turning public price data into a personal, explainable decision for India's smallholder farmers.**

Built for TetraTHON 2026 — AgriTech Track (Precision Crop Advisory & Post-Harvest Loss Reduction Planner)

---

## The Problem

Over 85% of India's farmers are smallholders, working under 2 hectares of land. Every year, 15–20% of what they grow rots before it ever reaches a buyer. This isn't a supply problem — India grows enough. It's a **decision problem**.

Farmers face two recurring challenges:
1. **Day-to-day crop care** — most rely on generic advice or guesswork for irrigation, fertilizer timing, and pest control, since personalized guidance rarely reaches them.
2. **Post-harvest decisions** — farmers bear the full cost of transporting produce to a mandi, sell through a commission agent with no visibility into better prices elsewhere, and often fall back on informal storage, losing value the longer produce waits.

## Our Solution

AgriNova is a two-engine decision-support web app:

### Crop Advisory Engine
Generates a day-wise, 7-day plan for irrigation, fertilizer, and pest control — based on crop type, soil type, sowing date, and live weather data. Not a flat weekly summary; each day's advisory adjusts to crop growth stage and confidence decreases transparently the further out the forecast goes.

### Sell / Store / Transport Planner
Compares three real outcomes for harvested crop:
- **Sell today** at the local mandi's current price
- **Store**, accounting for spoilage-driven value decay while waiting for a possible price rise
- **Transport** to a specific nearby mandi with a better price, weighed against real transport cost

Recommends whichever option nets the farmer the best return — visualized so the tradeoff is clear at a glance.

## Why Rule-Based, Not Black-Box AI

We deliberately built both engines on transparent, rule-based logic rather than an opaque ML model. Every recommendation shows its reasoning — the specific factor that drove the decision — so farmers can evaluate advice against their own judgment rather than blindly trust an algorithm. This directly addresses the real adoption barrier in agri-tech: **trust, not technology**.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** Responsive HTML/CSS/JS — no native app required, works on any farmer's existing smartphone browser
- **Database:** SQLite (local, reliable, no dependency on live government APIs)
- **Data:** Cleaned mandi price dataset sourced from [data.gov.in](https://data.gov.in) (Agmarknet)

## Getting Started

```bash
# Clone the repo
git clone https://github.com/explorer-2006/AgriNova.git
cd AgriNova

# Set up a virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run
```

Then open `http://localhost:5000` in your browser.

## Project Structure

AgriNova/
├── app.py # Flask entry point
├── static/ # CSS, JS, images
├── templates/ # HTML templates
├── data/ # Cleaned mandi price datasets
├── models/ # Rule engines (advisory + decision logic)
└── requirements.txt

## Roadmap

- Daily one-tap farmer feedback loop to adapt recommendations to real ground conditions
- SMS/WhatsApp price-threshold alerts
- Extending the decision engine into a multi-day, multi-mandi comparison as prediction confidence improves

## Team — FirstCommit

| Name | Role |
|---|---|
| Rudra Patel | Frontend & Design |
| Shivam Kamat | Frontend & Data Visualization |
| Meet Buddhdev | Backend & AI/ML Integration |
| Janisha Patel | Backend & Database Management |

---

*We're not building another agricultural marketplace. We're building the decision layer that's still missing — turning the same data India already collects into something a farmer can actually use, and actually trust.*
