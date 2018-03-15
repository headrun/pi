import httplib2
import os
from apiclient import discovery
from googleapiclient.http import *
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
#SCOPES = 'https://spreadsheets.google.com/feeds/'
SCOPES = 'https://spreadsheets.google.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
#CLIENT_SECRET_FILE = 'client_secret_json_forfb.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
class Googleupload(object):
	def main(self):
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		drive_service = discovery.build('drive', 'v2', http=http)
		media = MediaFileUpload('30k_linkedin_check.csv',mimetype='text/csv',resumable=True)	
		file_metadata = {
		 'title' : 'Sheet Name based on date and the type of profile',
		  'mimeType' : 'application/vnd.google-apps.spreadsheet'
		}
		files = drive_service.files().insert(body=file_metadata,media_body=media,fields='id').execute()
		print 'File ID: %s' % files.get('id')

	def get_credentials(self):
	    """Gets valid user credentials from storage.

	    If nothing has been stored, or if the stored credentials are invalid,
	    the OAuth2 flow is completed to obtain the new credentials.

	    Returns:
		Credentials, the obtained credential.
	    """
	    home_dir = os.path.expanduser('~')
	    credential_dir = os.path.join(home_dir, '.credentials')
	    if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	    credential_path = os.path.join(credential_dir,
					   'sheets.googleapis.com-python-quickstart.json')

	    store = Storage(credential_path)
	    credentials = store.get()
	    print credentials
	    #credentials = ''
	    if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
		    credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
		    credentials = tools.run(flow, store)
	    return credentials

if __name__ == '__main__':
    Googleupload().main()

