from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

Scopes = ['https://www.googleapis.com/auth/drive']
Keys = 'keys.json'

credentials = Credentials.from_service_account_file(Keys, scopes=Scopes)

drive_service = build('drive', 'v3', credentials=credentials)

def buscar_en_subcarpeta(carpeta_id, subcarpeta_nombre, nombre_documento):
    results = drive_service.files().list(
        q=f"'{carpeta_id}' in parents and name = '{subcarpeta_nombre}' and mimeType = 'application/vnd.google-apps.folder'",
        fields='files(id)'
    ).execute()

    subcarpetas = results.get('files', [])

    if subcarpetas:
        subcarpeta_id = subcarpetas[0]['id']

        results = drive_service.files().list(
            q=f"'{subcarpeta_id}' in parents and name = '{nombre_documento}'",
            fields='files(id)'
        ).execute()

        files = results.get('files', [])

        if files:
            file_id = files[0]['id']
            return file_id
        
def copiar_documento(file_id, carpeta_destino_id):
    if file_id is None:
        print("No se encontró el archivo a copiar.")
        return None
    
    file_metadata = {
        'parents': [carpeta_destino_id]
    }
    try:
        copied_file = drive_service.files().copy(
            fileId=file_id,
            body=file_metadata
        ).execute()

        print(f"Archivo copiado a la carpeta destino con ID: {copied_file['id']}")
        return copied_file['id']
    except Exception as error:
        print(f"Ocurrió un error al copiar el archivo: {error}")
        return None

def obtener_id_nuevo(nombre_documento, carpeta_id):
    results = drive_service.files().list(
        q=f"name = '{nombre_documento}' and '{carpeta_id}' in parents and trashed = false",
        fields='files(id, name, parents)'
    ).execute()

    files = results.get('files', [])

    if files:
        for file in files:
            if carpeta_id in file.get('parents', []):
                print(file['id'])
                return file['id']

    return None

def eliminar_doc(nombre_documento, carpeta_id):
    try:
        results = drive_service.files().list(
            q=f"name = '{nombre_documento}' and '{carpeta_id}' in parents and trashed = false",
            fields='files(id, name)'
        ).execute()
    except HttpError as error:
        print(f'Ha ocurrido un error al buscar el archivo: {error}')
        return

    files = results.get('files', [])

    if files:
        for file in files:
            try:
                drive_service.files().delete(fileId=file['id']).execute()
                print(f"El documento '{file['name']}' con ID {file['id']} ha sido eliminado.")
            except HttpError as error:
                print(f'No se pudo eliminar el documento {file["name"]} (ID: {file["id"]}): {error}')
    else:
        print("No se encontró el documento en la carpeta especificada.")