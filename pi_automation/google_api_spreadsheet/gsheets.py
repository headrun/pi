"""from gsheets import Sheets
sheets = Sheets.from_files('~/client_secrets.json', '~/storage.json')
print sheets"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

f = drive.CreateFile({'parent': parent_id})
f.SetContentFile('view.png') # Read local file
f.Upload()
