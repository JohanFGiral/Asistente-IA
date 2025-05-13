from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import os
from dotenv import load_dotenv
from app.stt import transcribir_audio
from app.mensaje import enviar_texto
from app.tts import texto_a_audio
import tempfile

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")



app = Flask(__name__)

@app.route('/audio/recibido/<filename>')
def servir_audio(filename):
    return send_from_directory('audio/recibido', filename)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route('/audio', methods=['POST'])
def audio():
    file = request.files['audio']
    
    # Guardar temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        file.save(temp_audio.name)
        temp_audio_path = temp_audio.name

    try:
        # Transcripción con Whisper
        texto = transcribir_audio(temp_audio_path)
    finally:
        os.remove(temp_audio_path)
        
    
    respuesta = enviar_texto(texto)
    ruta_audio = texto_a_audio(respuesta)
    nombre_archivo = os.path.basename(ruta_audio)
    print(respuesta)
    
    return jsonify({
        'reply': f"{texto}",
        'respuesta':f"{respuesta}",
        'audio': f"/audio/recibido/{nombre_archivo}"
        })


@app.route("/asistente", methods=["POST"])
def asistente():
    datos = request.get_json()
    mensaje_usuario = datos.get("mensaje", "")

    if not mensaje_usuario:
        return jsonify({"error": "Mensaje vacío"}), 400

    # Instrucción para modelos instruct-style
    instruccion = ("Actúa como una asistente llamada Mar-IA-na. "
    "Eres cordial, profesional y precisa. ")
    prompt = f"[INST] {instruccion} Usuario: {mensaje_usuario} [/INST]"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.8
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        salida = response.json()
        texto_generado = salida[0]["generated_text"].replace(prompt, "").strip()
        return jsonify({"respuesta": texto_generado})
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
