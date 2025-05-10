# riego/views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import TipoCultivo, TipoRiego, Cultivo, Cronograma, DetalleCronograma, Ubicacion
from .services.weather_service import get_centroid_lat_lon, obtener_datos_meteorologicos
from .services.cultivo_service import generar_cronograma_para_cultivo
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot.context import construir_contexto
from .chatbot.services import obtener_respuesta_ia

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_chatbot_cronograma(request, cultivo_id):
    mensaje = request.data.get("mensaje", "").strip()

    if not mensaje:
        return Response({"error": "No se envió un mensaje."}, status=400)

    try:
        cultivo = Cultivo.objects.get(id=cultivo_id, propietario=request.user)
        cronograma = Cronograma.objects.filter(cultivo=cultivo).order_by("-fecha_generacion").first()
        if not cronograma:
            return Response({"error": "No hay cronograma asociado a este cultivo."}, status=404)

        contexto = construir_contexto(cultivo)
        if not contexto or "resumen" not in contexto:
            return Response({"error": "No se pudo construir el contexto del cronograma."}, status=500)

        respuesta = obtener_respuesta_ia(contexto, mensaje)
        return Response({"respuesta": respuesta})
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Ver en consola
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_chatbot(request):
    mensaje = request.data.get("mensaje", "").strip()
    if not mensaje:
        return Response({"error": "Mensaje vacío"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        contexto = construir_contexto(request.user)
        respuesta = obtener_respuesta_ia(contexto, mensaje)
        return Response({"respuesta": respuesta})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generar_cronograma(request, cultivo_id):
    """
    Endpoint POST /cultivos/{cultivo_id}/generar-cronograma/
    1) Valida que el cultivo pertenezca al usuario.
    2) Calcula centroide de la ubicación.
    3) Trae datos de clima (ET₀ y precipitación) para 7 días.
    4) Elimina cualquier cronograma anterior si lo deseas.
    5) Llama al service para generar el cronograma real.
    6) Devuelve el cronograma serializado.
    """
    cultivo = get_object_or_404(Cultivo, pk=cultivo_id, propietario=request.user)

    # (Opcional) limpia cronogramas anteriores
    cultivo.cronogramas.all().delete()

    # 1) Lat/Lon desde su GeoJSON
    geojson = cultivo.ubicacion.coordenadas
    lat, lon = get_centroid_lat_lon(geojson)

    # 2) Obtiene clima para 7 días
    try:
        clima = obtener_datos_meteorologicos(lat, lon, days=7)
    except Exception as e:
        return Response(
            {'error': f'No se pudo obtener datos meteorológicos: {e}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # 3) Genera y guarda el cronograma real (incluye detalles con et_diario y precipitacion)
    try:
        cronograma = generar_cronograma_para_cultivo(cultivo, clima)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 4) Serializa y responde
    serializer = CronogramaSerializer(cronograma)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha_generacion']
    ordering = ['-fecha_generacion']

    def get_queryset(self):
        return Cronograma.objects.filter(cultivo__propietario=self.request.user)


class UbicacionViewSet(viewsets.ModelViewSet):
    serializer_class = UbicacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ubicacion.objects.filter(creada_por=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creada_por=self.request.user)
