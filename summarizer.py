import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    if len(text) > 4000:
        text = text[:4000]  # truncate to fit token limits

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following emails into concise bullet points."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']
