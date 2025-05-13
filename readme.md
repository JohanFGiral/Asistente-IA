# Asistente IA por Voz 🎙️💬

Este proyecto es un asistente conversacional que permite al usuario interactuar por texto o por voz, utilizando tecnologías de reconocimiento y síntesis de voz junto con modelos de lenguaje natural.

## ✨ Funcionalidades

- Reconocimiento de voz (Speech-to-Text) usando Whisper (Hugging Face).
- Respuesta inteligente generada por un modelo de lenguaje.
- Conversión de texto a voz (Text-to-Speech) usando ElevenLabs.
- Interfaz web sencilla con grabación de voz y respuestas habladas.

---

## ⚙️ Requisitos

- Python 3.10+
- Flask
- `requests`, `gtts` (si se usa alternativa), `dotenv`, etc.

## Tokens

Para instalar crea un archivo .env y coloca token de huggin face y de eleven labs usando las siguientes variables:
- ELEVEN_API_KEY=tu_token_de_elevenlabs.
- HF_TOKEN=tu_token_de_huggin_face.
---
Instalar dependencias:
```bash
pip install -r requirements.txt
