import openai
import requests
import os

openai.api_key = os.environ.get('OPENAI_KEY')

def descargar_audio(media_id):
    url_inicial = f"https://graph.facebook.com/v17.0/{media_id}"
    headers = {"Authorization": f"Bearer {os.environ.get('WHATSAPP_TOKEN')}"}

    response = requests.get(url_inicial, headers=headers)
    if response.status_code != 200:
        return "Error al obtener la URL del audio."

    data = response.json()
    url_audio = data.get("url")
    if not url_audio:
        return "No se encontró la URL del audio."

    response_audio = requests.get(url_audio, headers=headers)
    if response_audio.status_code == 200:
        with open(media_id+".mp3", "wb") as file:
            file.write(response_audio.content)
        audio_file = open(file.name, "rb")
        transcript = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
                )
        print(transcript)
        return transcript.text
    else:
        return "Error en la descarga del audio."

def eliminar_audio(nombre):
    try:
        os.remove(nombre)
        print(f"El archivo {nombre} ha sido eliminado con éxito.")
    except FileNotFoundError:
        print(f"El archivo {nombre} no se encontró.")
    except Exception as e:
        print(f"Error al eliminar el archivo {nombre}: {e}")