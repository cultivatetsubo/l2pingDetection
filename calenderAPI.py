from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def uploadfunc(Date,location,Name,beginTime,endTime):
  ID=os.environ.get('calendarID')
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  creds = None
      # The file token.pickle stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
  if os.path.exists('token.pickle'):
          with open('token.pickle', 'rb') as token:
              creds = pickle.load(token)
      # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
              creds.refresh(Request())
          else:
              flow = InstalledAppFlow.from_client_secrets_file(
                  'credentials.json', SCOPES)
              creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
          with open('token.pickle', 'wb') as token:
              pickle.dump(creds, token)

  service = build('calendar', 'v3', credentials=creds)
  event = {
          'summary': Name+"\t"+beginTime+" - "+endTime+"\t"+location,
          'location': None,
          'description': None,
          'start': {
              'date': Date,
              'timeZone': 'Japan',
          },
          'end': {
              'date': Date,
              'timeZone': 'Japan',
          },
          }
  event = service.events().insert(calendarId=ID,body=event).execute()
  print("uploadSuccess")
