import requests

url = "http://localhost:5000/asistente"

def enviar_texto(mensaje):
    mensaje = {"mensaje": mensaje}
    respuesta = requests.post(url,json=mensaje)
    
    if respuesta.status_code == 200:
        return (respuesta.json()["respuesta"])
    else:
        return ("Error:", respuesta.text)


