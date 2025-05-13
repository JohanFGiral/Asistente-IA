from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu")  # o "cuda" si tienes GPU

def transcribir_audio(ruta_archivo):
    segments, info = model.transcribe(ruta_archivo)
    texto_completo = ""

    for segment in segments:
        texto_completo += segment.text + " "  # concatenar texto de cada segmento

    return texto_completo.strip()

