from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    summary = summarizer_pipeline(text, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]
    return summary
