import httplib2
import os
import datetime
from apiclient import discovery
from googleapiclient.http import *
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
SCOPES = 'https://spreadsheets.google.com/feeds/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

class Googleupload(object):

	def arg_parse(self):
		try:
			import argparse
			flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			flags = None
		return flags
		
	def main(self, pf_type , emails_list, file_name):
		file_nam_split = ''
		if '.csv' in file_name:
			file_nam_split = file_nam_split.split('.csv')[0]
		elif '.xls' in file_name:
			file_nam_split = file_nam_split.split('.xls')[0]
		dic_folder_ids = {'paytm_session_data':'10lUW0_WV_zNKqKULe-Gfj4gtglqDTy71','paytm':'1btTwrYeyK006KLMb-TPciLPJx-wgHP16','bookmyshow':'1-tZnz2XAygWbIC1U6gRHe6oYDLEAeGgh','ticketnew':'1CXbD6A-1drsGmdiDUScA80lh068mE2ZD'}
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		drive_service =  discovery.build('drive', 'v2', http=http,cache_discovery=False)
		response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",spaces='drive',pageToken=None).execute()
		folders_list = [(item['title']) for item in response['items']]
		today = datetime.datetime.now()
		today_month = today.strftime('%B')
		file_metadata = {
			'title' :file_name,
			'mimeType' : 'application/vnd.google-apps.spreadsheet',
			}
		months_folders = [(item['title']) for item in response['items'] if dic_folder_ids[pf_type] in item['parents'][0]['parentLink']]
		if today_month in months_folders:
			folder_id_today = [(item['id']) for item in response['items'] if dic_folder_ids[pf_type] in item['parents'][0]['parentLink'] and item['title']==today_month]
			if folder_id_today:
				folder_id_today = folder_id_today[0]
				file_metadata.update({'parents': [{'id':folder_id_today}]})
		else:
			folder_meta = {"title":today_month, 'mimeType' : 'application/vnd.google-apps.folder', 'parents': [{'id':dic_folder_ids[pf_type]}]}
			new_folder_name = drive_service.files().insert(body=folder_meta,fields='id').execute()
			if new_folder_name:
				file_metadata.update({'parents': [{'id':new_folder_name.get('id','')}]})
		mimetype_ = 'text/csv'
		if '.xls' in file_name:
			mimetype_ = 'application/vnd.ms-excel'
		media = MediaFileUpload(file_name, mimetype=mimetype_, resumable=True)	
		files = drive_service.files().insert(body=file_metadata,media_body=media,fields='id').execute()
		return files.get('id')

	def get_credentials(self):
	    """Gets valid user credentials from storage.

	    If nothing has been stored, or if the stored credentials are invalid,
	    the OAuth2 flow is completed to obtain the new credentials.

	    Returns:
		Credentials, the obtained credential.
	    """
	    home_dir = os.path.expanduser('~')
	    credential_dir = os.path.join(home_dir, '.credentialspositive')
	    if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	    credential_path = os.path.join(credential_dir,
					   'sheets.googleapis.com-python-quickstart.json')

	    store = Storage(credential_path)
	    credentials = store.get()
	    if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		flags = self.arg_parse()
		if flags:
		    credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
		    credentials = tools.run(flow, store)
	    return credentials

if __name__ == '__main__':
    Googleupload().main('', '', '')

