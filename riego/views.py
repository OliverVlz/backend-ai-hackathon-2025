# riego/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TipoCultivo, TipoRiego, Cultivo, Cronograma, DetalleCronograma, Ubicacion
from .serializers import (
    RegistroUsuarioSerializer, TipoCultivoSerializer, TipoRiegoSerializer,
    CultivoSerializer, CronogramaSerializer, DetalleCronogramaSerializer, UbicacionSerializer, UserProfileSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite registro sin autenticación
def registro_usuario(request):
    try:
        print(f"Datos recibidos: {request.data}")
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
        print(f"Errores de validación: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error en registro_usuario: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({'message': 'Bienvenido a la API de AiRiego'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


# ViewSets para los modelos principales
class TipoCultivoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoCultivoSerializer
    queryset = TipoCultivo.objects.all()
    permission_classes = [IsAuthenticated]


class TipoRiegoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoRiegoSerializer
    queryset = TipoRiego.objects.all()
    permission_classes = [IsAuthenticated]


class CultivoViewSet(viewsets.ModelViewSet):
    serializer_class = CultivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cultivo.objects.filter(propietario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)


class CronogramaViewSet(viewsets.ModelViewSet):
    serializer_class = CronogramaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cronograma.objects.filter(cultivo__propietario=self.request.user)


# Vista para generar un nuevo cronograma para un cultivo específico
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generar_cronograma(request, cultivo_id):
    try:
        cultivo = Cultivo.objects.get(id=cultivo_id, propietario=request.user)

        # Aquí iría la lógica para obtener datos climáticos y calcular necesidades de agua
        # Por ahora, generamos un cronograma de ejemplo

        # Crear cronograma
        cronograma = Cronograma.objects.create(
            cultivo=cultivo,
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

    except Cultivo.DoesNotExist:
        return Response({"error": "Cultivo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class UbicacionViewSet(viewsets.ModelViewSet):
    serializer_class = UbicacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ubicacion.objects.filter(creada_por=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creada_por=self.request.user)
