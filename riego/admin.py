from django.contrib import admin
from .models import TipoCultivo, TipoRiego, ZonaCultivo, Cronograma, DetalleCronograma

@admin.register(TipoCultivo)
class TipoCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'coef_plantula', 'coef_adulto', 'coef_anciano', 'es_predefinido')
    search_fields = ('nombre',)

@admin.register(TipoRiego)
class TipoRiegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'eficiencia')

@admin.register(ZonaCultivo)
class ZonaCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_cultivo', 'etapa_crecimiento', 'tipo_riego', 'area', 'creado_por')
    search_fields = ('nombre', 'creado_por__username', 'tipo_cultivo__nombre')
    list_filter = ('tipo_cultivo', 'etapa_crecimiento', 'tipo_riego', 'activo', 'creado_por')



@admin.register(Cronograma)
class CronogramaAdmin(admin.ModelAdmin):
    list_display = ('zona_cultivo', 'fecha_generacion', 'fecha_inicio')
    list_filter = ('fecha_generacion', 'fecha_inicio')
    search_fields = ('zona_cultivo__nombre',)

@admin.register(DetalleCronograma)
class DetalleCronogramaAdmin(admin.ModelAdmin):
    list_display = ('cronograma', 'dia', 'fecha', 'hora_inicio', 'duracion_horas', 'cantidad_agua')
    list_filter = ('dia', 'fecha')

# Register your models here.
