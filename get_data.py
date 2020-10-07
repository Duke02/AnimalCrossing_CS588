"""
This file uses the Google Sheets API to gather community supplied data from
the Twitter user @KnightCarmine. You can find the original dataset (and the
Twitter post I got it from) here - https://twitter.com/KnightCarmine/status/1249397162405801984
"""
import os.path
import pickle
import typing as tp

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Only perform read only operations on the spreadsheet.
from island_week_data import IslandWeekData

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the community data spreadsheet.
SPREADSHEET_ID = '1hMmewPJvXw-tmabvccC0nWJdN7zw3aQIQzN3EQ9is6g'
CELL_RANGE = 'Archive!C:S'


def get_api_key(filepath: str) -> str:
    with open(filepath, 'r') as f:
        return f.readline().strip()


def get_credentials(filepath: str, cached_location: str = 'token.pickle'):
    """
    Gets the credentials at the provided location. Reads the cached_location for previous credentials.
    Writes to cached_location if credentials are remade.
    :param filepath: The filepath to the json file containing application credentials.
    :param cached_location: The filepath to the pickled file storing previous credentials from previous runs of the application.
    :return: The credentials accepted by the Google API Service.
    """
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cached_location):
        with open(cached_location, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                filepath, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cached_location, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


def get_raw_data(service, spreadsheet_id: str = SPREADSHEET_ID, range: str = CELL_RANGE) -> tp.List:
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    return result.get('values', [])


def parse_row(row: tp.List[str]) -> IslandWeekData:
    """
    Parses the row directly from the spreadsheet and restructures it into an IslandWeekData
    :param row: the sample row directly from the spreadsheet that contains the owner, the island, the prices, the purchase price, and the patterns (previous and current)
    """
    pass


def main():
    credentials = get_credentials('resources/credentials.json')
    service = build('sheets', 'v4', credentials=credentials)

    rows: list = get_raw_data(service)

    if not rows:
        print('No data found.')
        return

    # TODO: Need to figure out the week number of the spreadsheet.
    # The week number is incremented each time there is a completely different row.
    structured_data: tp.List[IslandWeekData] = [parse_row(row) for row in rows]


if __name__ == '__main__':
    main()
