from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TipoCultivo, TipoRiego, ZonaCultivo, Cronograma, DetalleCronograma

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
    class Meta:
        model = TipoCultivo
        fields = ['id', 'nombre', 'descripcion', 'coef_plantula', 'coef_adulto', 'coef_anciano', 'es_predefinido']


class TipoRiegoSerializer(serializers.ModelSerializer):
    nombre_display = serializers.SerializerMethodField()
    
    class Meta:
        model = TipoRiego
        fields = ['id', 'nombre', 'nombre_display', 'eficiencia']
    
    def get_nombre_display(self, obj):
        return obj.get_nombre_display()


class ZonaCultivoSerializer(serializers.ModelSerializer):
    creado_por = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ZonaCultivo
        fields = ['id', 'nombre', 'coordenadas', 'area', 'creado_por', 'fecha_creacion',
                  'tipo_cultivo', 'etapa_crecimiento', 'tipo_riego', 'tasa_flujo', 'activo']
        read_only_fields = ['fecha_creacion']
    
    def create(self, validated_data):
        # Asignar el usuario actual como creador
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)


class DetalleCronogramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCronograma
        fields = ['id', 'dia', 'fecha', 'hora_inicio', 'duracion_horas', 'cantidad_agua',
                  'et_diario', 'precipitacion']


class CronogramaSerializer(serializers.ModelSerializer):
    detalles = DetalleCronogramaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cronograma
        fields = ['id', 'zona_cultivo', 'fecha_generacion', 'fecha_inicio',
                  'et_promedio', 'precipitacion_promedio', 'detalles']
        read_only_fields = ['fecha_generacion']