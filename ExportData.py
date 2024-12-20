from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os

def ExportData(folder_id, file_name, mime_type, folder_path):
    CLIENT = os.environ.get("CLIENT")
    API_NAME = os.environ.get("API_NAME")
    API_VERSION = os.environ.get("API_VERSION")
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    service = Create_Service(CLIENT, API_NAME, API_VERSION, SCOPES)

    for file_name, mime_type in zip(file_name, mime_type):
        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
        }

    media = MediaFileUpload(f"{folder_path}" + f"{file_name}", mimetype=mime_type)

    service.files().create(
        body = file_metadata,
        media_body = media,
        fields = "id"
    ).execute()

    print("Export Data Success")