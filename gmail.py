from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64

# Script is altered version of the one provided in the official documentation.

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Directory path of this file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Your credentials.json that you download from Google Cloud Platform
CREDENTIAL_FILE = dir_path + '/credentials.json'
TOKEN_FILE = dir_path + '/token.pickle'
USERNAME_FILE = dir_path + '/username.txt'

username = ''
with open(USERNAME_FILE, 'r') as f:
    username = f.read().strip()

FROM_EMAIL = username
TO_EMAIL = username

def init():
    """ Authenticate with GMail API.
    """

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIAL_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print('Authenticated')
            return
    else:
        print('Already authenticated')
    

def mail(subject, message_text):
    """Send mail using GMail API.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    else:
        print('Not authenticated, run init()')

    service = build('gmail', 'v1', credentials=creds)

    message = create_message(FROM_EMAIL, TO_EMAIL, subject, message_text)

    print('Attempting to send message...')
    try:
        send_message(service, TO_EMAIL, message)
    except Exception as e:
        print('Failed due to: ', e)
    print('Success!')


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    # https://github.com/googleapis/google-api-python-client/issues/93
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
