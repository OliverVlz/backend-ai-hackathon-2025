from openai import OpenAI
from django.conf import settings
from .constants import SYSTEM_PROMPT, PROMPT_CULTIVO

client = OpenAI(
    api_key=settings.QWEN_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

def obtener_respuesta_ia(contexto, mensaje):
    # Rellenar el prompt con los datos del contexto y el mensaje del usuario
    
    prompt = PROMPT_CULTIVO.format(
        ubicacion=contexto['ubicacion'],
        tipo_cultivo=contexto['tipo_cultivo'],
        etapa_crecimiento=contexto['etapa_crecimiento'],
        kc=contexto['kc'],
        fecha_inicio=contexto['fecha_inicio'],
        consumo_agua_diario=contexto['consumo_agua_diario'],
        lluvia_promedio_diaria=contexto['lluvia_promedio_diaria'],
        horas_riego_promedio=contexto['horas_riego_promedio'],
        alertas="\n".join(contexto['alertas']) if contexto['alertas'] else '✅ Todo parece estar bien hasta ahora.',
        mensaje=mensaje
    )
    
    # Llamada a la API de OpenAI (o Qwen)
    completion = client.chat.completions.create(
        model="qwen-turbo",  # o el modelo que estés usando
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # Contexto general, si lo tienes
            {"role": "user", "content": prompt}  # Mensaje generado por el usuario
        ]
    )
    return completion.choices[0].message.content
