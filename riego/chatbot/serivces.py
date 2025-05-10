# riego/chatbot/context.py
from models import *

def construir_contexto(usuario) -> str:
    cultivos = Cultivo.objects.filter(usuario=usuario).prefetch_related('cronograma_set')
    texto = 'Eres un asistente de riego inteligente. Estos son los cultivos y sus cronogramas: '
    for c in cultivos:
        texto += f"Cultivo {c.nombre}: "
        for cron in c.cronograma_set.all():
            texto += f"[{cron.fecha}: {cron.tarea}], "
    return texto