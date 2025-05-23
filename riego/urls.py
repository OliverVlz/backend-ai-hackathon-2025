from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Configurar router para ViewSets
router = DefaultRouter()
router.register(r'tipos-cultivo', TipoCultivoViewSet, basename='tipocultivo')
router.register(r'tipos-riego', TipoRiegoViewSet, basename='tiporiego')
router.register(r'cultivos', CultivoViewSet, basename='cultivo')
router.register(r'cronogramas', CronogramaViewSet, basename='cronograma')
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')

urlpatterns = [
    path('', home, name='home'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),  # protegida por token
    path('cultivos/<int:cultivo_id>/generar-cronograma/', generar_cronograma, name='generar_cronograma'),
    path('chatbot/', api_chatbot, name='api_chatbot'),
    path('chatbot/cultivos/<int:cultivo_id>/preguntar/', api_chatbot_cronograma, name='api_chatbot_cronograma'),
    path('', include(router.urls)),
]
