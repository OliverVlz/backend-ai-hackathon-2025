from django.urls import path
from .views import home, registro_usuario, perfil_usuario

urlpatterns = [
    path('', home, name='home'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),  # protegida por token
]
