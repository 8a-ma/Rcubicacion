import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.cloud import storage
from google.oauth2 import service_account
import datetime

def import_token(file):
    storage_client = storage.Client(os.environ.get("STORAGE_CLIENT"))
    bucket = storage_client.get_bucket(os.environ.get("BUCKET"))
    blob = bucket.blob(f"{file}")
    blob.download_to_filename(f"/tmp/{file}")
    print("Credentials downladed on /tmp/")

def Create_Service(client_secret_file, api_name, api_version, *scopes):

    print(client_secret_file, api_name, api_version, scopes, sep='-')

    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    print(SCOPES)
    
    import_token("serviceAccount.json")
    
    cred = service_account.Credentials.from_service_account_file(
            filename=CLIENT_SECRET_FILE,
            scopes = SCOPES
        )

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service

    except Exception as e:
        return f'Unable to connect. {e}'

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt