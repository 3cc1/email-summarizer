import requests
from datetime import datetime, timedelta
import base64
import email


def get_emails(access_token, days, keywords=""):
    headers = {"Authorization": f"Bearer {access_token}"}
    date_since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y/%m/%d")
    query = f"after:{date_since}"
    if keywords:
        query += f" {keywords}"

    list_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages?q={query}"
    resp = requests.get(list_url, headers=headers)
    messages = resp.json().get("messages", [])[:5]

    full_text = ""
    for msg in messages:
        msg_id = msg["id"]
        msg_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=full"
        msg_data = requests.get(msg_url, headers=headers).json()

        parts = msg_data.get("payload", {}).get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                decoded = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("utf-8", errors="ignore")
                full_text += decoded + "\n"
                break

    return full_text
