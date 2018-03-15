from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentialspositive')
    print(credential_dir)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    #spreadsheetId = '1U4fAzlnmpytNCYdVgirlz5uXUEeGPT-K4qN2iyDCZJ0'
    #spreadsheetId = '1kIzfQg9k2NHlvQxjmF227f0XOe3qYCjTuu6-BGydV6Y'
    #spreadsheetId = '1qyVUMi3-VdTBl0Jh41_30RVhTTn6OBE-jItemR6lgIs'
    #spreadsheetId = '182T-LLFOMYiOHl2Up2qVVb7kDJ-kHvvdM-vcVLLdzGY'
    #spreadsheetId = '1NqO1G2tFD9RryuBWaUjRWBD7-MUHC_BCnVOEYbJhAKg'
    #spreadsheetId = '1pAXeVn8lWX3WCOGq_O0VHDAyCW-pDoZ16RMqJj0ZLVM'
    #spreadsheetId = '1A99KEXAHKsvTS-jXLmcjXGH0B9TkEdrM1uHdsZKdpaA'
    #spreadsheetId = '1pAXeVn8lWX3WCOGq_O0VHDAyCW-pDoZ16RMqJj0ZLVM'
    spreadsheetId = '1J6ePSWKbJkwfsr2xohmks9S03wThDT23jQvftDcbVdk'
    #rangeName = 'Class Data!A2:E'
    rangeName = 'E:F'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    #result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId).execute()
    to_check = []
    values = result.get('values', [])
    city_list = [val[0] for val in values]
    set_cit = set(city_list)
    print(len(set_cit))

if __name__ == '__main__':
    main()

