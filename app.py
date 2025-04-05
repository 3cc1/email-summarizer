from flask import Flask, request, jsonify
from summarizer import summarize_emails

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    keywords = request.form.get("keywords", "")
    folder = request.form.get("folder", "inbox")
    days = int(request.form.get("time", 7))  # Days ago

    try:
        summary = summarize_emails(folder, days, keywords)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500