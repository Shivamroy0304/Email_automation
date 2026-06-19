
import asyncio
import html
import os

from telegram import Bot
from twilio.rest import Client


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def make_voice_call(summary: str) -> None:
    """Trigger a Twilio voice call with the summary.

    This function is synchronous and will print errors instead of raising so
    the notifier flow continues even when Twilio fails.
    """
    try:
        twilio_sid = _get_required_env("TWILIO_SID")
        twilio_auth_token = _get_required_env("TWILIO_AUTH_TOKEN")
        twilio_phone_number = _get_required_env("TWILIO_PHONE_NUMBER")
        your_phone_number = _get_required_env("YOUR_PHONE_NUMBER")

        client = Client(twilio_sid, twilio_auth_token)
        message = summary or "Hello Shivam, please check your important email."
        escaped_message = html.escape(message)
        call = client.calls.create(
            twiml=f"<Response><Say>{escaped_message}</Say></Response>",
            to=your_phone_number,
            from_=twilio_phone_number,
        )
        # call.sid may or may not exist depending on error/response
        sid = getattr(call, "sid", None)
        print("Call initiated with SID:", sid)
    except Exception as e:
        print("Twilio call failed:", repr(e))


def _send_telegram_sync(summary: str) -> None:
    """Send a Telegram message in a way that works for both sync and async Bot implementations.

    Some versions of python-telegram-bot expose an async send_message (coroutine)
    while others are synchronous. This wrapper detects that and uses
    asyncio.run when needed.
    """
    try:
        telegram_token = _get_required_env("TELEGRAM_TOKEN")
        chat_id = _get_required_env("CHAT_ID")
        bot = Bot(token=telegram_token)
        result = bot.send_message(chat_id=chat_id, text=summary)
        # If the library returned a coroutine, run it
        if asyncio.iscoroutine(result):
            asyncio.run(result)
    except Exception as e:
        # Another attempt using asyncio.run in case bot.send_message itself is a coroutine function
        try:
            telegram_token = _get_required_env("TELEGRAM_TOKEN")
            chat_id = _get_required_env("CHAT_ID")
            bot = Bot(token=telegram_token)
            coro = bot.send_message(chat_id=chat_id, text=summary)
            if asyncio.iscoroutine(coro):
                asyncio.run(coro)
            else:
                # If it's not a coroutine and still raised, re-raise to outer except
                raise
        except Exception as e2:
            print("Telegram send failed:", repr(e2))


def send_summary(summary: str) -> None:
    """Public synchronous function used by main.py.

    It will attempt to send a Telegram message and then trigger the voice call.
    """
    _send_telegram_sync(summary)
    # Always try the call even if Telegram fails
    make_voice_call(summary)
