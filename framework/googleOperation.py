from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)



def read_sheet(sheet_id, range_name):
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name
    ).execute()
    return result.get("values", [])

def write_sheet(sheet_id, range_name, values):
    service = get_service()
    body = {"values": values}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
