# riego/chatbot/services.py
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def obtener_respuesta_ia(mensaje_usuario: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente de prueba."},
            {"role": "user", "content": mensaje_usuario},
        ]
    )
    return response.choices[0].message.content
