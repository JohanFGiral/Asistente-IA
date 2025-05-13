import os
import requests
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

VOICE_ID = "n4x17EKVqyxfey8QMqvy"
STABILITY = 0.90
SIMILARITY = 0.81
SPEED = 1.06

OUTPUT_DIR = "audio/recibido"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def texto_a_audio(texto, nombre_archivo=None):
    # Generar nombre con timestamp si no se proporciona
    if not nombre_archivo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"respuesta_{timestamp}.mp3"

    output_path = os.path.join(OUTPUT_DIR, nombre_archivo)
    if not texto:
        raise ValueError ("Texto vacío")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": STABILITY,
            "similarity_boost": SIMILARITY,
            "style": 0,
            "use_speaker_boost": True,
            "speed": SPEED
        }
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Error en TTS: {response.status_code} - {response.text}")
    
if __name__ == "__main__":
    texto_prueba = "Hola, soy Lina. Esta es una prueba de voz."
    texto_a_audio(texto_prueba)