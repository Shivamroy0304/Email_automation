from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

creds = None
if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

service = build("gmail", "v1", credentials=creds)
res = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=5).execute()
msgs = res.get('messages', [])
print('found', len(msgs))
for m in msgs:
    d = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
    headers = d['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name']=='Subject'), '')
    sender = next((h['value'] for h in headers if h['name']=='From'), '')
    print('---')
    print('id', m['id'])
    print('from', sender)
    print('subject', subject)
