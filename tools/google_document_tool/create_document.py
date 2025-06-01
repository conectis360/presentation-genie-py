from google.oauth2 import service_account
from googleapiclient.discovery import build
import argparse

# Configurações necessárias
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'service-account.json'  # Arquivo de credenciais


def create_google_document(text, title="Novo Documento"):
    """
    Cria um Google Document com o texto fornecido

    Args:
        text (str): Conteúdo do documento
        title (str): Título do documento (padrão: "Novo Documento")
    """
    # Autenticação
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # Criação do serviço
    service = build('docs', 'v1', credentials=credentials)

    # Cria documento em branco
    document = service.documents().create(body={'title': title}).execute()
    doc_id = document['documentId']
    print(f"Documento criado! ID: {doc_id}")
    print(f"Acesse em: https://docs.google.com/document/d/{doc_id}")

    # Insere o texto no documento
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1  # Insere no início do documento
                },
                'text': text
            }
        }
    ]

    service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    print("Texto inserido com sucesso!")