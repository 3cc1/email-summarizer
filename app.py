import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    app.run(debug=True)
