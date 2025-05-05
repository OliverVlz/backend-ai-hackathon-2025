from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, registro_usuario, perfil_usuario, generar_cronograma,
    TipoCultivoViewSet, TipoRiegoViewSet, CultivoViewSet, CronogramaViewSet, UbicacionViewSet
)

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
    path('', include(router.urls)),
]
