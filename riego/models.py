# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import time
from shapely.geometry import shape
from shapely.ops import transform
import pyproj

class TipoCultivo(models.Model):
    nombre = models.CharField(max_length=100, unique=False)
    descripcion = models.TextField(blank=True)
    # Coeficientes para diferentes etapas
    coef_plantula = models.FloatField(default=0.0)
    coef_crecimiento = models.FloatField(default=0.0)
    coef_madurez = models.FloatField(default=0.0)
    es_predefinido = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class TipoRiego(models.Model):
    TIPOS = [
        ('superficial', 'Superficial'),
        ('aspersion', 'Aspersión'),
        ('goteo', 'Goteo'),
        ('subterraneo', 'Subterráneo'),
    ]
    
    nombre = models.CharField(max_length=100, choices=TIPOS)
    eficiencia = models.FloatField(help_text="Eficiencia del sistema de riego (valor decimal entre 0 y 1, por ejemplo 0.75 para 75%)")
    
    def __str__(self):
        return self.get_nombre_display()
    
    def save(self, *args, **kwargs):
        # Asignar valores predeterminados de eficiencia según el tipo
        if self.eficiencia in [None, 0]:
            if self.nombre == 'superficial':
                self.eficiencia = 0.45  # 45%
            elif self.nombre == 'aspersion':
                self.eficiencia = 0.75  # 75%
            elif self.nombre == 'goteo':
                self.eficiencia = 0.92  # 92%
            elif self.nombre == 'subterraneo':
                self.eficiencia = 0.87  # 87%
        super().save(*args, **kwargs)

class Ubicacion(models.Model):
    coordenadas = models.JSONField(help_text="Coordenadas GeoJSON del polígono")
    area = models.FloatField(help_text="Área en metros cuadrados (calculada con Shapely)")
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ubicaciones"

    def save(self, *args, **kwargs):
        # Calcular área en m² usando Shapely y pyproj
        try:
            poligono = shape(self.coordenadas)
        except Exception as e:
            raise ValueError(f"Coordenadas inválidas: {e}")
        lon, lat = poligono.centroid.x, poligono.centroid.y
        utm_zone = int((lon + 180) / 6) + 1
        is_northern = lat >= 0
        utm_crs = f'+proj=utm +zone={utm_zone} +{"north" if is_northern else "south"} +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
        project = pyproj.Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True).transform
        poligono_utm = transform(project, poligono)
        self.area = poligono_utm.area
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ciudad}, {self.pais}"

class Cultivo(models.Model):
    ETAPAS = [
        ('plantula', 'Plántula'),
        ('crecimiento', 'Crecimiento'),
        ('madurez', 'Madurez'),
    ]
    
    nombre = models.CharField(max_length=200)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, related_name='cultivos')
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.PROTECT)
    etapa_crecimiento = models.CharField(max_length=20, choices=ETAPAS)
    tipo_riego = models.ForeignKey(TipoRiego, on_delete=models.PROTECT)
    tasa_flujo = models.FloatField(help_text="Tasa de flujo en galones/hora")
    activo = models.BooleanField(default=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cultivos')

    def __str__(self):
        return f"{self.nombre} ({self.tipo_cultivo.nombre})"

class Cronograma(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='cronogramas')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    # Datos meteorológicos usados para el cálculo
    et_promedio = models.FloatField(null=True, blank=True)
    precipitacion_promedio = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Cronograma para {self.cultivo} - {self.fecha_inicio}"

class DetalleCronograma(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE, related_name='detalles')
    dia = models.IntegerField(help_text="Día del cronograma (1-7)")
    fecha = models.DateField()
    hora_inicio = models.TimeField(default=time(22, 0))  # 10 PM por defecto
    duracion_horas = models.FloatField(help_text="Duración en horas")
    cantidad_agua = models.FloatField(help_text="Cantidad de agua en galones")
    et_diario = models.FloatField(null=True, blank=True)
    precipitacion = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['dia']
    
    def __str__(self):
        return f"Día {self.dia} - {self.fecha}"
