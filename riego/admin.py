from django.contrib import admin
from .models import TipoCultivo, TipoRiego, Cultivo, Cronograma, DetalleCronograma, Ubicacion

@admin.register(TipoCultivo)
class TipoCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'coef_plantula', 'coef_adulto', 'coef_anciano', 'es_predefinido')
    search_fields = ('nombre',)

@admin.register(TipoRiego)
class TipoRiegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'eficiencia')
    search_fields = ('nombre',)

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('pais', 'ciudad', 'area', 'creada_por', 'fecha_creacion')
    search_fields = ('pais', 'ciudad', 'creada_por__username')
    list_filter = ('pais', 'ciudad', 'creada_por')

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_cultivo', 'etapa_crecimiento', 'tipo_riego', 'tasa_flujo', 'activo', 'propietario')
    search_fields = ('nombre', 'propietario__username', 'tipo_cultivo__nombre')
    list_filter = ('tipo_cultivo', 'etapa_crecimiento', 'tipo_riego', 'activo', 'propietario')

@admin.register(Cronograma)
class CronogramaAdmin(admin.ModelAdmin):
    list_display = ('cultivo', 'fecha_generacion', 'fecha_inicio')
    list_filter = ('fecha_generacion', 'fecha_inicio')
    search_fields = ('cultivo__nombre',)

@admin.register(DetalleCronograma)
class DetalleCronogramaAdmin(admin.ModelAdmin):
    list_display = ('cronograma', 'dia', 'fecha', 'hora_inicio', 'duracion_horas', 'cantidad_agua')
    list_filter = ('cronograma', 'fecha')
    search_fields = ('cronograma__cultivo__nombre',)

# Register your models here.
