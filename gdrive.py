from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import os.path
from pathlib import Path
import progressbar

SHARED_DRIVE_ID = "0AJgwtlVQm-JQUk9PVA"
ROOT_FOLDER_ID = "17wGYvqdbXFs_U47XpB89Rcu9DYWrPl4L"

# Define the scopes required for Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDrive():
    def __init__(self):
        self.service = self.authenticate_google_drive()
        self.get_sub_folders()

    def authenticate_google_drive(self):
        """Authenticate and create the Google Drive service."""
        creds = None

        # Load existing credentials from the token.json file
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If no valid credentials available, request the user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # Connect to the Google Drive API
        service = build('drive', 'v3', credentials=creds)
        return service

    def get_sub_folders(self):
        self.sub_folders = {}
        service = self.service
        page_token = None
        while True:
            response = service.files().list(
                q=f"'{ROOT_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
                spaces='drive',
                corpora='drive',
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                driveId=SHARED_DRIVE_ID,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()

            for file in response.get('files', []):
                self.sub_folders[file.get("name")] = file.get("id")

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break


    def create_folder(self, folder_name):
        service = self.service
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [ROOT_FOLDER_ID]
        }

        folder = service.files().create(body=file_metadata, supportsAllDrives=True, fields='id').execute()
        print(f'Destination Folder created: {folder_name} (ID: {folder.get("id")})')

        self.sub_folders[folder_name] = folder.get("files", [])

    def upload_file(self, path_to_file, folder_name):
        service = self.service

        if folder_name in self.sub_folders.keys():
            folder_id = self.sub_folders[folder_name]
        else:
            folder_id = self.create_folder(folder_name)

        filename = Path(path_to_file).name

        file_metadata = {
        'name': filename,
        'parents': [folder_id],
        }

        print(f"Uploading '{path_to_file}' to '{folder_name}/'")
        media = MediaFileUpload(path_to_file, resumable=True, chunksize=1*1024**2)
        file_size = media.size()

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            supportsAllDrives=True,
            fields='id'
        )

        progress_bar = progressbar.ProgressBar(maxval=file_size)
        progress_bar.start()

        # Upload the file in chunks and update the progress bar
        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                progress_bar.update(status.resumable_progress)

        progress_bar.finish()


