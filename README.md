# Email Automation and Alerting

This project checks Gmail for unread messages from important senders and can notify you in two ways:

- Send a Telegram message with the email summary.
- Place a Twilio voice call that reads the alert aloud.

It is designed to keep personal credentials and API secrets out of the repository.

## Features

- Gmail unread-mail scanning.
- Sender-based filtering for important emails.
- Telegram notification support.
- Twilio voice-call support.
- Local-only credential handling for Gmail OAuth and API secrets.

## Project Layout

- `main.py` handles Gmail authentication and unread email scanning.
- `notifier.py` sends Telegram notifications and Twilio voice calls.
- `run.py` starts the main email-check flow.
- `twilo.py` is a local Twilio smoke test.
- `setup.py` contains packaging settings.

## Requirements

- Python 3.10 or newer.
- A Google account with Gmail API access enabled.
- A Telegram bot token and chat ID.
- A Twilio account, phone number, and auth token.

## Installation

1. Create and activate a virtual environment.
2. Install the project dependencies.
3. Copy `.env.example` to `.env` and fill in your secrets.

Example:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install twilio python-telegram-bot google-api-python-client google-auth-oauthlib google-auth requests streamlit python-dotenv langchain transformers
cp .env.example .env
```

## Configuration

The notifier reads these environment variables:

- `TELEGRAM_TOKEN`
- `CHAT_ID`
- `TWILIO_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `YOUR_PHONE_NUMBER`
- `VOICE_CALL_MESSAGE`

For Gmail authentication, keep your local OAuth files outside version control:

- `credentials.json`
- `token.json`

## Usage

Run the email automation flow:

```bash
python run.py
```

Run the Twilio smoke test:

```bash
python twilo.py
```

## Security Notes

- Do not commit `.env`, `credentials.json`, or `token.json`.
- Regenerate any secret that has already been exposed.
- If you have previously committed secrets to Git history, rewrite the history before publishing publicly.

## GitHub Publishing

After reviewing the files locally, you can publish with:

```bash
git init
git add .
git commit -m "Initial email automation project"
git branch -M main
git remote add origin https://github.com/Shivamroy0304/Email_automation.git
git push -u origin main
```

If the repository already exists locally, skip `git init`.