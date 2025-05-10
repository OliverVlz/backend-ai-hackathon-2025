from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TipoCultivo, TipoRiego, Cultivo, Cronograma, DetalleCronograma, Ubicacion

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya existe.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TipoCultivoSerializer(serializers.ModelSerializer):
    def validate_coef_plantula(self, value):
        if not (0 <= value <= 2):
            raise serializers.ValidationError("El coeficiente de plántula debe estar entre 0 y 2.")
        return value

    def validate_coef_crecimiento(self, value):
        if not (0 <= value <= 2):
            raise serializers.ValidationError("El coeficiente de crecimiento debe estar entre 0 y 2.")
        return value

    def validate_coef_madurez(self, value):
        if not (0 <= value <= 2):
            raise serializers.ValidationError("El coeficiente de madurez debe estar entre 0 y 2.")
        return value

    class Meta:
        model = TipoCultivo
        fields = '__all__'


class TipoRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRiego
        fields = '__all__'

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'
        read_only_fields = ['area', 'creada_por', 'fecha_creacion']
class CultivoSerializer(serializers.ModelSerializer):
    tipo_cultivo_info = TipoCultivoSerializer(source='tipo_cultivo', read_only=True)
    tipo_riego_info = TipoRiegoSerializer(source='tipo_riego', read_only=True)
    ubicacion_info = UbicacionSerializer(source='ubicacion', read_only=True)
    def validate_tasa_flujo(self, value):
        if value <= 0:
            raise serializers.ValidationError("La tasa de flujo debe ser mayor a 0.")
        return value

    class Meta:
        model = Cultivo
        fields = '__all__'
        read_only_fields = ['propietario']


class DetalleCronogramaSerializer(serializers.ModelSerializer):
    cantidad_agua_gal = serializers.SerializerMethodField()
    duracion_formateada = serializers.SerializerMethodField()

    class Meta:
        model = DetalleCronograma
        fields = [
            'id', 'dia', 'fecha', 'hora_inicio',
            'duracion_horas', 'cantidad_agua',
            'cantidad_agua_gal', 'duracion_formateada',
            'et_diario', 'precipitacion',
        ]
        read_only_fields = fields

    def get_cantidad_agua_gal(self, obj):
        return round(obj.cantidad_agua / 3.78541, 2)

    def get_duracion_formateada(self, obj):
        horas = int(obj.duracion_horas)
        minutos = round((obj.duracion_horas - horas) * 60)
        return f"{horas}h {minutos}min"

class CronogramaSerializer(serializers.ModelSerializer):
    cultivo_nombre = serializers.CharField(source='cultivo.nombre', read_only=True)
    ubicacion = serializers.SerializerMethodField()  # Cambiar a SerializerMethodField
    detalles = DetalleCronogramaSerializer(many=True, read_only=True)

    class Meta:
        model = Cronograma
        fields = [
            'id', 'cultivo', 'cultivo_nombre', 'ubicacion',
            'fecha_generacion', 'fecha_inicio',
            'et_promedio', 'precipitacion_promedio',
            'detalles',
        ]
        read_only_fields = ['id', 'fecha_generacion', 'detalles', 'cultivo_nombre', 'ubicacion']

    def get_ubicacion(self, obj):
        # Combinar ciudad y país
        ciudad = obj.cultivo.ubicacion.ciudad if obj.cultivo.ubicacion else None
        pais = obj.cultivo.ubicacion.pais if obj.cultivo.ubicacion else None
        if ciudad and pais:
            return f"{ciudad}, {pais}"
        elif ciudad:
            return ciudad
        elif pais:
            return pais
        return "Ubicación desconocida"