# riego/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TipoCultivo, TipoRiego, ZonaCultivo, Cronograma, DetalleCronograma
from .serializers import (
    RegistroUsuarioSerializer, TipoCultivoSerializer, TipoRiegoSerializer,
    ZonaCultivoSerializer, CronogramaSerializer, DetalleCronogramaSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite registro sin autenticación
def registro_usuario(request):
    serializer = RegistroUsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({'message': 'Bienvenido a la API de AiRiego'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Requiere autenticación
def perfil_usuario(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })


# ViewSets para los modelos principales
class TipoCultivoViewSet(viewsets.ModelViewSet):
    queryset = TipoCultivo.objects.all()
    serializer_class = TipoCultivoSerializer
    permission_classes = [IsAuthenticated]


class TipoRiegoViewSet(viewsets.ModelViewSet):
    queryset = TipoRiego.objects.all()
    serializer_class = TipoRiegoSerializer
    permission_classes = [IsAuthenticated]


class ZonaCultivoViewSet(viewsets.ModelViewSet):
    serializer_class = ZonaCultivoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar zonas por usuario autenticado
        return ZonaCultivo.objects.filter(creado_por=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)


class CronogramaViewSet(viewsets.ModelViewSet):
    serializer_class = CronogramaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar cronogramas por usuario autenticado
        return Cronograma.objects.filter(zona_cultivo__creado_por=self.request.user)


# Vista para generar un nuevo cronograma para una zona específica
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generar_cronograma(request, zona_id):
    try:
        zona = ZonaCultivo.objects.get(id=zona_id, creado_por=request.user)
        
        # Aquí iría la lógica para obtener datos climáticos y calcular necesidades de agua
        # Por ahora, generamos un cronograma de ejemplo
        
        # Crear cronograma
        cronograma = Cronograma.objects.create(
            zona_cultivo=zona,
            fecha_inicio=timezone.now().date()
        )
        
        # Crear detalles de ejemplo
        for i in range(1, 8):
            DetalleCronograma.objects.create(
                cronograma=cronograma,
                dia=i,
                fecha=timezone.now().date() + timezone.timedelta(days=i-1),
                hora_inicio="22:00",
                duracion_horas=2.5,
                cantidad_agua=500 * i  # Valor de ejemplo
            )
        
        serializer = CronogramaSerializer(cronograma)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except ZonaCultivo.DoesNotExist:
        return Response({"error": "Zona de cultivo no encontrada"}, status=status.HTTP_404_NOT_FOUND)
