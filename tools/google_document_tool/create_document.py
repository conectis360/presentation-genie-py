from google.oauth2 import service_account
from googleapiclient.discovery import build
import argparse


# Configurações necessárias
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'service-account.json'  # Arquivo de credenciais


def create_google_document(text: str, title: str):
    """
    Creates a new Google Document with the provided text content.

    This function creates a blank Google Document with the specified title,
    then inserts the provided text content into the document. The function
    handles authentication using service account credentials and returns
    comprehensive information about the operation result.

    Args:
        text (str): The text content to be inserted into the document
        title (str): The title for the new Google Document
        service_account_path (str): Optional path to service account JSON file.
                                  If not provided, will look for:
                                  1. 'service-account.json' in current directory
                                  2. 'credentials.json' in current directory
                                  3. GOOGLE_APPLICATION_CREDENTIALS environment variable

    Returns:
        dict: A dictionary containing:
            - status (str): Operation status ("success" or "error")
            - document_id (str): The unique ID of the created document (if successful)
            - document_url (str): Direct URL to access the document (if successful)
            - message (str): Descriptive message about the operation
            - error_details (str): Detailed error information (if error occurred)
            - credentials_path (str): Path to credentials file used (if successful)
    """
    try:
        # Find service account file
        credentials_file = None

        if service_account_path:
            # Use provided path
            if os.path.exists(service_account_path):
                credentials_file = service_account_path
            else:
                return {
                    "status": "error",
                    "message": "Service account file not found at specified path",
                    "error_details": f"File not found: {service_account_path}",
                    "document_id": None,
                    "document_url": None,
                    "credentials_path": None
                }
        else:
            # Try common file names and locations
            possible_files = [
                'service-account.json',
                'credentials.json',
                os.path.expanduser('~/service-account.json'),
                os.path.expanduser('~/credentials.json')
            ]

            # Also check environment variable
            env_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if env_creds:
                possible_files.insert(0, env_creds)

            for file_path in possible_files:
                if os.path.exists(file_path):
                    credentials_file = file_path
                    break

        if not credentials_file:
            return {
                "status": "error",
                "message": "No valid service account credentials file found",
                "error_details": "Searched for: service-account.json, credentials.json, GOOGLE_APPLICATION_CREDENTIALS environment variable",
                "document_id": None,
                "document_url": None,
                "credentials_path": None
            }

        # Validate JSON file
        try:
            with open(credentials_file, 'r') as f:
                json.load(f)
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Invalid JSON format in credentials file",
                "error_details": f"File {credentials_file} is not valid JSON",
                "document_id": None,
                "document_url": None,
                "credentials_path": credentials_file
            }

        # Authentication
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )

        # Create service
        service = build('docs', 'v1', credentials=credentials)

        # Create blank document
        document = service.documents().create(body={'title': title}).execute()
        doc_id = document['documentId']

        # Insert text into document
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1  # Insert at the beginning of document
                    },
                    'text': text
                }
            }
        ]

        service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        # Return success response
        return {
            "status": "success",
            "document_id": doc_id,
            "document_url": f"https://docs.google.com/document/d/{doc_id}",
            "message": f"Successfully created Google Document '{title}' with provided content",
            "text_length": len(text),
            "credentials_path": credentials_file
        }

    except Exception as e:
        # Return error response
        return {
            "status": "error",
            "message": "Failed to create Google Document",
            "error_details": str(e),
            "document_id": None,
            "document_url": None,
            "credentials_path": getattr(locals(), 'credentials_file', None)
        }
