from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'googleapiclient',
        'google_auth_oauthlib',
        'google.oauth2',
        'twilio',
        'telegram',
        'http',
        'urllib3',
    ],
    'includes': ['notifier', 'categorize'],
    'plist': {
        'CFBundleName': 'Email Notifier',
        'CFBundleShortVersionString': '0.1.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
