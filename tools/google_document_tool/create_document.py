import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Docs API configuration
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'service-account.json'  # Arquivo de credenciais


def create_google_document(text: str, title: str):
    """
    Creates a new Google Document with the provided text content.

    This function creates a blank Google Document with the specified title
    and inserts the provided text content. It automatically searches for
    service account credentials in common locations.

    Args:
        text (str): The text content to be inserted into the document
        title (str): The title for the new Google Document

    Returns:
        dict: A dictionary containing:
            - status (str): "success" or "error"
            - document_id (str): The unique ID of the created document
            - document_url (str): Direct URL to access the document
            - message (str): Descriptive message about the operation result
            - error_details (str): Error information if operation failed
    """
    try:
        # Lista de possíveis locais de credenciais (com caminhos absolutos)
        possible_files = []

        # 1. Variável de ambiente (prioridade máxima)
        env_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if env_creds:
            possible_files.append(os.path.abspath(env_creds))

        # 2. Diretório atual do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_files.extend([
            os.path.join(script_dir, 'service-account.json'),
            os.path.join(script_dir, 'credentials.json')
        ])

        # 3. Diretório de trabalho atual
        cwd = os.getcwd()
        if cwd != script_dir:  # Evitar duplicatas
            possible_files.extend([
                os.path.join(cwd, 'service-account.json'),
                os.path.join(cwd, 'credentials.json')
            ])

        # 4. Diretório home do usuário
        try:
            home_dir = os.path.expanduser('~')
            possible_files.extend([
                os.path.join(home_dir, 'service-account.json'),
                os.path.join(home_dir, 'credentials.json')
            ])
        except Exception:
            pass

        # Remover duplicatas e verificar existência
        checked_files = []
        credentials_file = None
        for file_path in possible_files:
            # Normalizar caminhos e remover duplicatas
            abs_path = os.path.abspath(file_path)
            if abs_path not in checked_files:
                checked_files.append(abs_path)
                if os.path.exists(abs_path):
                    credentials_file = abs_path
                    break

        # Se nenhum arquivo foi encontrado
        if not credentials_file:
            checked_paths = "\n".join(f"- {path}" for path in checked_files)
            return {
                "status": "error",
                "message": "Arquivo de credenciais não encontrado",
                "error_details": f"Locais verificados:\n{checked_paths}",
                "document_id": "",
                "document_url": ""
            }

        # Validate credentials file
        try:
            with open(credentials_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "Invalid credentials file format",
                "error_details": f"The file {credentials_file} is not valid JSON",
                "document_id": "",
                "document_url": ""
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Cannot read credentials file",
                "error_details": f"Error reading {credentials_file}: {str(e)}",
                "document_id": "",
                "document_url": ""
            }

        # Authenticate with Google APIs
        try:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_file, scopes=SCOPES
            )
        except Exception as e:
            return {
                "status": "error",
                "message": "Authentication failed",
                "error_details": f"Failed to authenticate with {credentials_file}: {str(e)}",
                "document_id": "",
                "document_url": ""
            }

        # Create Google Docs service
        try:
            service = build('docs', 'v1', credentials=credentials)
        except Exception as e:
            return {
                "status": "error",
                "message": "Failed to create Google Docs service",
                "error_details": f"Service creation error: {str(e)}",
                "document_id": "",
                "document_url": ""
            }

        # Create blank document
        try:
            document = service.documents().create(body={'title': title}).execute()
            doc_id = document['documentId']
        except Exception as e:
            return {
                "status": "error",
                "message": "Failed to create document",
                "error_details": f"Document creation error: {str(e)}",
                "document_id": "",
                "document_url": ""
            }

        # Insert text into document
        try:
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
        except Exception as e:
            return {
                "status": "error",
                "message": "Failed to insert text into document",
                "error_details": f"Text insertion error: {str(e)}",
                "document_id": doc_id,
                "document_url": f"https://docs.google.com/document/d/{doc_id}"
            }

        # Return success response
        return {
            "status": "success",
            "document_id": doc_id,
            "document_url": f"https://docs.google.com/document/d/{doc_id}",
            "message": f"Google Document '{title}' created successfully with {len(text)} characters",
            "error_details": ""
        }

    except Exception as e:
        # Catch any unexpected errors
        return {
            "status": "error",
            "message": "Unexpected error occurred",
            "error_details": f"Unexpected error: {str(e)}",
            "document_id": "",
            "document_url": ""
        }

