"""Small local smoke test for the Twilio voice call flow.

This file depends on the same environment variables used by notifier.py.
"""

import os

from notifier import make_voice_call


if __name__ == "__main__":
    message = os.getenv("VOICE_CALL_MESSAGE", "Hello Shivam, please check your important email.")
    make_voice_call(message)
