import main
from google.oauth2.credentials import Credentials

print('Invoking gmail_authenticate()')
service = main.gmail_authenticate()
print('Authenticated, calling get_unread_emails')
main.get_unread_emails(service)
print('Done')
