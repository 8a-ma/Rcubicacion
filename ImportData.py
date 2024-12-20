from google.auth.transport import requests
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload
import os
import io

def ImportData(file_id, file_name, path):
    CLIENT = os.environ.get("CLIENT")
    API_NAME = os.environ.get("API_NAME")
    API_VERSION = os.environ.get("API_VERSION")
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    service = Create_Service(CLIENT, API_NAME, API_VERSION, SCOPES)

    try:
        request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%" % int(status.progress() *100))
    except Exception:
        request = service.files().export(
            fileId= file_id,
            mimeType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%" % int(status.progress() *100))
        
        return False
    
    with open(os.path.join(path, "{0}".format(file_name)), "wb") as f:
        fh.seek(0)
        f.write(fh.read())

    print("Import Success")