import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env
openai.api_key = os.getenv("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")

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following emails into concise bullet points."},
            {"role": "user", "content": text}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
