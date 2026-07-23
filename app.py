"""
Mandi Price App — Flask backend
Stack: Flask + SQLite + vanilla HTML/CSS/JS
Data source: Agmarknet mandi price dataset (data.gov.in), cleaned and stored locally.
"""

import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify

app = Flask(__name__)
app.secret_key = "change-this-in-production"

DB_PATH = Path(__file__).parent / "mandi.db"

SUPPORTED_LANGS = {"en", "hi", "gu"}


# ---------- Database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Run once to create tables. `flask --app app init-db` or call from a shell."""
    with app.app_context():
        db = get_db()
        with open(Path(__file__).parent / "schema.sql") as f:
            db.executescript(f.read())
        db.commit()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Initialized SQLite database at", DB_PATH)


# ---------- Routes ----------
@app.route("/")
def index():
    # If user already picked a language, skip welcome.
    if session.get("lang") in SUPPORTED_LANGS:
        return redirect(url_for("home"))
    return redirect(url_for("welcome"))


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html", current_lang=session.get("lang"))


@app.route("/set-language", methods=["POST"])
def set_language():
    """Called by welcome.js when the user taps Continue."""
    data = request.get_json(silent=True) or {}
    lang = data.get("lang")
    if lang not in SUPPORTED_LANGS:
        return jsonify({"ok": False, "error": "unsupported language"}), 400
    session["lang"] = lang
    return jsonify({"ok": True, "redirect": url_for("dashboard")})


@app.route("/home")
def home():
    # Kept as a stable alias; the real landing screen is the dashboard.
    return redirect(url_for("dashboard"))


# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    # Static weather block — no API call, per spec.
    weather = {
        "location": "Vadodara, Gujarat",
        "temp": 29,
        "condition": "Sunny",
        "rain_chance": 20,
        "icon": "\u2600\ufe0f",
    }
    return render_template(
        "dashboard.html",
        user_name=session.get("user_name", "Rudra"),
        weather=weather,
        active_tab="home",
    )


# ---------- Placeholder screens ----------
@app.route("/harvest")
def harvest():
    return render_template(
        "placeholder.html",
        page_title="Harvest Decision",
        page_icon="\U0001F4E6",
        page_subtitle="Sell \u2022 Store \u2022 Transport",
        page_message=(
            "Mandi price comparison and sell-or-store guidance will appear here."
        ),
        active_tab="harvest",
    )


@app.route("/settings")
def settings():
    return render_template(
        "placeholder.html",
        page_title="Settings",
        page_icon="\u2699\ufe0f",
        page_subtitle="Language, profile and preferences",
        page_message="Profile details and language preferences will appear here.",
        active_tab="settings",
    )


# ---------- Crop Advisory flow ----------
@app.route("/farm-details", methods=["GET"])
def farm_details():
    return render_template("farm_details.html")


@app.route("/farm-details", methods=["POST"])
def save_farm_details():
    """Called by farm-details.js when the user taps 'Generate 7-Day Plan'."""
    data = request.get_json(silent=True) or {}
    required = ("crop", "district", "soil_type", "sowing_date")
    if not all(data.get(k) for k in required):
        return jsonify({"ok": False, "error": "missing fields"}), 400

    session["farm"] = {
        "crop": data["crop"],
        "district": data["district"],
        "soil_type": data["soil_type"],
        "sowing_date": data["sowing_date"],
    }
    return jsonify({"ok": True, "redirect": url_for("crop_advisory")})


@app.route("/crop-advisory")
def crop_advisory():
    farm = session.get("farm")
    if not farm:
        return redirect(url_for("farm_details"))

    # TODO: replace this static plan with a real recommendation engine
    # driven by soil_type / sowing_date / local weather + mandi data.
    week_plan = [
        {"label": "Mon", "icon": "\U0001F4A7", "action": "Water", "active": True},
        {"label": "Tue", "icon": "\U0001F331", "action": "Fertilizer", "active": False},
        {"label": "Wed", "icon": "\U0001F7E0", "action": "Monitor", "active": False},
        {"label": "Thu", "icon": "\U0001F41B", "action": "Pest Check", "active": False},
        {"label": "Fri", "icon": "\U0001F4A7", "action": "Water", "active": False},
        {"label": "Sat", "icon": "\U0001F33E", "action": "No Action", "active": False},
        {"label": "Sun", "icon": "\U0001F331", "action": "Fertilizer", "active": False},
    ]

    tasks = [
        {
            "icon": "\U0001F4A7",
            "title": "Irrigation",
            "desc": "Water for approximately 35-40 minutes during early morning or evening.",
            "tag": "Recommended",
            "tag_style": "pill--accent",
        },
        {
            "icon": "\U0001F331",
            "title": "Fertilizer",
            "desc": "No fertilizer required today.",
            "tag": "Skip Today",
            "tag_style": "",
        },
        {
            "icon": "\U0001F50D",
            "title": "Pest Monitoring",
            "desc": "Inspect lower leaves for early pest activity.",
            "tag": "Quick Check",
            "tag_style": "",
        },
    ]

    reasons = [
        "Warm temperatures increase water loss.",
        "No rainfall is expected today.",
        "Your {} crop is currently in an active growth stage.".format(farm["crop"]),
    ]

    return render_template(
        "crop_advisory.html",
        farm=farm,
        week_plan=week_plan,
        tasks=tasks,
        confidence=92,
        reasons=reasons,
        tomorrow_url="#",  # wire up once a tomorrow-plan route exists
    )


if __name__ == "__main__":
    app.run(debug=True)
