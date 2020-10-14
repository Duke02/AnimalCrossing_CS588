"""
This file uses the Google Sheets API to gather community supplied data from
the Twitter user @KnightCarmine. You can find the original dataset (and the
Twitter post I got it from) here - https://twitter.com/KnightCarmine/status/1249397162405801984
"""
import os.path
import pickle
import typing as tp

import numpy as np
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Only perform read only operations on the spreadsheet.
import utility
from constants import *
from island_week_data import IslandWeekData, TurnipPattern


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
    # A lot of this code is from https://developers.google.com/sheets/api/quickstart/python
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


def parse_row(row: tp.List[str], week_number: int) -> tp.Union[None, IslandWeekData]:
    """
    Parses the row directly from the spreadsheet and restructures it into an IslandWeekData
    :param row: the sample row directly from the spreadsheet that contains the owner, the island, the prices, the purchase price, and the patterns (previous and current)
    """
    try:
        owner: str = row[0]
        island_name: str = row[1]

        if len(row[2]) < 1:
            raise Exception('Purchase price is empty.')
        purchase_price: int = int(row[2])

        end_of_prices: int = 15

        raw_prices: tp.List[tp.Union[str, None]] = [price if len(price) > 0 else None for price in row[3:end_of_prices]]
        prices: tp.List[tp.Union[None, int]] = [int(p) if type(p) == str and p.isdigit() else None for p in raw_prices]

        current_pattern: TurnipPattern = utility.get_pattern(row[end_of_prices]) if len(
            row) > end_of_prices else TurnipPattern.EMPTY
        previous_pattern: TurnipPattern = utility.get_pattern(row[end_of_prices + 1]) if len(row) > (
                end_of_prices + 1) else TurnipPattern.EMPTY

        return IslandWeekData(owner, island_name, week_number, prices, purchase_price, previous_pattern,
                              current_pattern)
    except Exception as e:
        print(f'Parsing row caused an exception: {e}')
        print(f'Row is: {row}')
        print(f'Returning {None}')
        return None


def main():
    credentials = get_credentials('resources/credentials.json')
    service = build('sheets', 'v4', credentials=credentials)

    rows: list = get_raw_data(service)

    if not rows:
        print('No data found.')
        return

    structured_data: tp.List[IslandWeekData] = []
    week_num: int = 0

    cleaned_rows: tp.List[tp.List[str]] = []

    for row in rows:
        if all([len(cell) < 1 for cell in row]):
            week_num += 1
        else:
            parsed_row: tp.Union[None, IslandWeekData] = parse_row(row, week_num)
            if parsed_row:
                cleaned_rows.append(row)
                structured_data.append(parsed_row)

    data: np.ndarray = utility.island_data_to_numpy(structured_data)
    print(data.shape)


if __name__ == '__main__':
    main()
