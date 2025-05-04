from django.db import models
from django.contrib.auth.models import User

class TipoCultivo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    # Coeficientes para diferentes etapas
    coef_plantula = models.FloatField(default=0.0)
    coef_adulto = models.FloatField(default=0.0)
    coef_anciano = models.FloatField(default=0.0)
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
    eficiencia = models.FloatField(help_text="Eficiencia en porcentaje (0-100)")
    
    def __str__(self):
        return self.get_nombre_display()
    
    def save(self, *args, **kwargs):
        # Asignar valores predeterminados de eficiencia según el tipo
        if not self.eficiencia:
            if self.nombre == 'superficial':
                self.eficiencia = 45  # 45%
            elif self.nombre == 'aspersion':
                self.eficiencia = 75  # 75%
            elif self.nombre == 'goteo':
                self.eficiencia = 92  # 92%
            elif self.nombre == 'subterraneo':
                self.eficiencia = 87  # 87%
        
        super().save(*args, **kwargs)

class ZonaCultivo(models.Model):
    ETAPAS = [
        ('plantula', 'Plántula'),
        ('adulto', 'Adulto'),
        ('anciano', 'Anciano'),
    ]
    
    nombre = models.CharField(max_length=200)
    # Por ahora usamos un campo de texto para las coordenadas
    # En una versión futura podríamos usar GeoDjango
    coordenadas = models.TextField(help_text="Coordenadas en formato JSON")
    area = models.FloatField(help_text="Área en metros cuadrados", null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zonas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Campos que estaban en Cultivo
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.PROTECT, null=True, blank=True)
    etapa_crecimiento = models.CharField(max_length=20, choices=ETAPAS, null=True, blank=True)
    tipo_riego = models.ForeignKey(TipoRiego, on_delete=models.PROTECT, null=True, blank=True)
    tasa_flujo = models.FloatField(help_text="Tasa de flujo en galones/hora", null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        tipo = self.tipo_cultivo.nombre if self.tipo_cultivo else "Sin cultivo"
        return f"{self.nombre} - {tipo}"

class Cronograma(models.Model):
    zona_cultivo = models.ForeignKey(ZonaCultivo, on_delete=models.CASCADE, related_name='cronogramas')
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
    hora_inicio = models.TimeField(default='22:00')  # 10 PM por defecto
    duracion_horas = models.FloatField(help_text="Duración en horas")
    cantidad_agua = models.FloatField(help_text="Cantidad de agua en galones")
    et_diario = models.FloatField(null=True, blank=True)
    precipitacion = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['dia']
    
    def __str__(self):
        return f"Día {self.dia} - {self.fecha}"
