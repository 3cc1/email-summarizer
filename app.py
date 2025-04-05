import os
import json
import requests
from flask import Flask, redirect, request, session, url_for, jsonify
from summarizer import summarize_text
from gmail import get_emails
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:5000/oauth2callback")

SCOPES = "https://www.googleapis.com/auth/gmail.readonly"


@app.route("/")
def index():
    return "Email Summarizer Backend Running ✅"


@app.route("/login")
def login():
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    tokens = r.json()
    session["access_token"] = tokens["access_token"]
    return redirect(url_for("summary_ui"))


@app.route("/summary-ui")
def summary_ui():
    return """
    <form method="POST" action="/summarize">
        <input name="keywords" placeholder="Keywords (optional)" />
        <select name="days">
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="180">Last 6 months</option>
        </select>
        <button type="submit">Summarize Emails</button>
    </form>
    """


@app.route("/summarize", methods=["POST"])
def summarize():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))

    days = int(request.form.get("days", 7))
    keywords = request.form.get("keywords", "")

    try:
        email_text = get_emails(access_token, days, keywords)
        if not email_text:
            return "No matching emails found."
        summary = summarize_text(email_text[:3000])  # limit length
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500