# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "student_data.csv"

# ensure data file exists with header
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "subject", "topic", "confidence", "score", "advice"])

def generate_advice(confidence: int, score: int) -> str:
    """
    Simple rule-based adaptive logic:
    - confidence: 1 (low) .. 5 (high)
    - score: 0 .. 100
    """
    if confidence >= 4 and score < 65:
        return "Overconfident but low score — add extra practice problems: 30–45 min daily + timed quizzes twice a week."
    if confidence <= 2 and score >= 75:
        return "Performing well but low confidence — do short weekly mocks (20–30 min) and quick daily flashcards to build confidence."
    if score < 50:
        return "Weak performance — focus on concept revision: 2 short revision sessions daily (25 mins each) + solved examples."
    if 50 <= score < 70:
        return "Average performance — mix concept revision with problem practice; weekly full test recommended."
    return "Good performance — maintain with timed practice tests weekly and targeted revision for tricky topics."

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/plan", methods=["POST"])
def plan():
    # form fields: subject, topic, confidence (1-5), score (0-100)
    subject = request.form.get("subject", "").strip()
    topic = request.form.get("topic", "").strip()
    try:
        confidence = int(request.form.get("confidence", "3"))
    except ValueError:
        confidence = 3
    try:
        score = int(request.form.get("score", "0"))
    except ValueError:
        score = 0

    advice = generate_advice(confidence, score)
    timestamp = datetime.utcnow().isoformat()

    # Append to CSV
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, subject, topic, confidence, score, advice])

    # Render result page with plan
    return render_template("result.html",
                           subject=subject,
                           topic=topic,
                           confidence=confidence,
                           score=score,
                           advice=advice)

@app.route("/history", methods=["GET"])
def history():
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
    # Show latest first
    entries = list(reversed(entries))
    return render_template("history.html", entries=entries)

if __name__ == "__main__":
    # debug True for development; on macOS local use default host/port
    app.run(debug=True)
