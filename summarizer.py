import imaplib
import email
from datetime import datetime, timedelta
from transformers import pipeline

summarizer_pipeline = pipeline("summarization")

EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

def summarize_emails(folder, days, keyword):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    mail.select(folder)

    date_since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    search_criteria = f'(SINCE "{date_since}")'
    if keyword:
        search_criteria = f'(BODY "{keyword}" SINCE "{date_since}")'

    status, data = mail.search(None, search_criteria)
    email_ids = data[0].split()

    full_text = ""
    for e_id in email_ids[-5:]:  # Only summarize last 5 matching emails
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                full_text += part.get_payload(decode=True).decode(errors="ignore")
                break

    if not full_text:
        return "No matching emails found."

    result = summarizer_pipeline(full_text[:3000])[0]["summary_text"]
    return result