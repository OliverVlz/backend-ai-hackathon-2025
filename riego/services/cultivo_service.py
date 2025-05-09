# riego/services/cultivo_service.py

from datetime import datetime, time
from django.utils import timezone
from riego.models import Cronograma, DetalleCronograma

def generar_cronograma_para_cultivo(cultivo, clima: list[dict]) -> Cronograma:
    """
    Genera un cronograma de riego para un cultivo, usando datos climáticos.

    :param cultivo: instancia de Cultivo
    :param clima: lista de dicts con 'fecha', 'et0', 'precipitacion' (uno por día)
    :return: instancia de Cronograma creada
    """

    # 1) Coeficiente Kc según etapa
    etapa = cultivo.etapa_crecimiento
    kc = {
        'plantula': cultivo.tipo_cultivo.coef_plantula,
        'crecimiento': cultivo.tipo_cultivo.coef_crecimiento,
        'madurez': cultivo.tipo_cultivo.coef_madurez,
    }.get(etapa, cultivo.tipo_cultivo.coef_crecimiento)

    eficiencia = cultivo.tipo_riego.eficiencia
    area_m2    = cultivo.ubicacion.area
    flujo_lph  = cultivo.tasa_flujo

    # 2) Crear el objeto Cronograma
    fecha_inicio = datetime.strptime(clima[0]['fecha'], "%Y-%m-%d").date()
    et_prom = sum(d['et0'] for d in clima) / len(clima)
    pr_prom = sum(d['precipitacion'] for d in clima) / len(clima)

    cronograma = Cronograma.objects.create(
        cultivo=cultivo,
        fecha_generacion=timezone.now(),
        fecha_inicio=fecha_inicio,
        et_promedio=et_prom,
        precipitacion_promedio=pr_prom,
    )

    # 3) Detalles diarios
    for idx, dia in enumerate(clima, start=1):
        et0       = dia['et0']
        precip    = dia['precipitacion']

        # Evapotranspiración ajustada
        etc       = et0 * kc

        # Agua neta/mm sobre la parcela
        agua_neta_mm = max(etc - precip, 0)

        # Agua bruta conteniendo pérdida por eficiencia
        agua_bruta_mm = agua_neta_mm / eficiencia

        # Volumen en litros
        litros = agua_bruta_mm * area_m2

        # Convertir litros a galones
        galones = litros / 3.785

        # Tiempo de riego (horas)
        duracion_h = galones / flujo_lph  if flujo_lph > 0 else 0

        DetalleCronograma.objects.create(
            cronograma=cronograma,
            dia=idx,
            fecha=dia['fecha'],
            hora_inicio=time(22, 0),
            duracion_horas=duracion_h,
            cantidad_agua=galones,
            et_diario=et0,
            precipitacion=precip,
        )

    return cronograma
