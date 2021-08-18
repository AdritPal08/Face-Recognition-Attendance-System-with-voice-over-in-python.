from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
upload_file = 'face_encode.txt'
gfile = drive.CreateFile({'parents': [{'id': '16RC-BBWp5B69YE9KUSgjhqmzDz_bkaH6'}]})
# Read file and set it as the content of this instance.
gfile.SetContentFile(upload_file)
gfile.Upload() # Upload the file.