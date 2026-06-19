import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from notifier import send_summary, make_voice_call
import base64
import re
from setuptools import setup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


IMPORTANT_SENDERS = {
    #"noreply.cdcinfo@vitstudent.ac.in",
    #"vitianscdc2026@vitstudent.ac.in",
    #"info@content.goibibo.com"
    #"student@updates.internshala.com"
    #"linkedin@em.linkedin.com"
    "vrajgovani253@gmail.com"
}
KEYWORD = "Hii"



def normalize_text(text: str) -> str:
    """Lowercase and remove punctuation for more robust matching."""
    if not text:
        return ""
    text = text.lower()
    return re.sub(r"[^a-z0-9\s]", "", text).strip()


def extract_body_from_payload(payload: dict) -> str:
    """Recursively extract text/plain body from the message payload.

    Falls back to joining any text/plain parts found. If none, returns an empty string.
    """
    parts = []

    def walk(part):
        mime = part.get('mimeType', '')
        if mime == 'text/plain' and 'body' in part and part['body'].get('data'):
            parts.append(part['body']['data'])
        for sub in part.get('parts', []) or []:
            walk(sub)

    walk(payload)

    if not parts:
        return ""

    body = ""
    for p in parts:
        try:
            body += base64.urlsafe_b64decode(p).decode('utf-8', errors='ignore')
        except Exception:
            continue
    return body

def gmail_authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def get_unread_emails(service):
    print('DEBUG: get_unread_emails started')
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).execute()
    messages = results.get('messages', [])

    print(f"You have {len(messages)} unread email(s).")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "")
        snippet = msg_data.get("snippet", "")

        
        match = re.search(r"<(.+?)>", sender)
        email_cleaned = (match.group(1).lower() if match else sender.lower())

        try:
            body = extract_body_from_payload(msg_data['payload'])
            if not body:
                body = snippet
        except Exception:
            body = snippet

        # Check if email is from important sender (no keyword check needed)
        sender_match = email_cleaned in IMPORTANT_SENDERS

        if sender_match:
            print("Important email from VIT found! Triggering call and Telegram...")
            message = f"📧 From: {email_cleaned}\nSubject: {subject}\n\n{snippet}"
            send_summary(message)
            make_voice_call(message)
        else:
            print("Skipping email:")
            print("  From header:", sender)
            print("  Parsed email:", email_cleaned)
            print("  Subject:", subject)
            print("  Sender matched:", sender_match)

