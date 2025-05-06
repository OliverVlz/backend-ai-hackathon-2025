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


class CultivoSerializer(serializers.ModelSerializer):
    def validate_tasa_flujo(self, value):
        if value <= 0:
            raise serializers.ValidationError("La tasa de flujo debe ser mayor a 0.")
        return value

    class Meta:
        model = Cultivo
        fields = '__all__'
        read_only_fields = ['propietario']


class DetalleCronogramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCronograma
        fields = '__all__'


class CronogramaSerializer(serializers.ModelSerializer):
    detalles = DetalleCronogramaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cronograma
        fields = ['id', 'cultivo', 'fecha_generacion', 'fecha_inicio',
                  'et_promedio', 'precipitacion_promedio', 'detalles']
        read_only_fields = ['fecha_generacion']


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'
        read_only_fields = ['area', 'creada_por', 'fecha_creacion']