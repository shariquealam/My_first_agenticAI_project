
from framework.googleAuthenticator import GoogleAuthenticator

class GoogleOperation:

    def __init__(self):
        self.googleAuthObject = GoogleAuthenticator()

    # def read_sheet(self,sheet_id, range_name):
    def read_sheet(self, sheet_id):
        service = self.googleAuthObject.get_google_service()
        result = service.spreadsheets().values().get(
            # spreadsheetId=sheet_id, range=range_name
        spreadsheetId = sheet_id
        ).execute()
        return result.get("values", [])

    # def write_sheet(self,sheet_id, range_name, values):
    def write_sheet(self, sheet_id, values):
        service = self.googleAuthObject.get_google_service()
        body = {"values": values}
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            # range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
