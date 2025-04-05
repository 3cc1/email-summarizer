from transformers import pipeline

summarizer_pipeline = pipeline("summarization")

def summarize_text(text):
    summary = summarizer_pipeline(text)[0]["summary_text"]
    return summary
