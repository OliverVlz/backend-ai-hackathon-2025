from ..models import *

def construir_contexto(cultivo):
    cronograma = cultivo.cronogramas.order_by("-fecha_generacion").first()
    if not cronograma:
        return {}

    detalles = cronograma.detalles.order_by('fecha')
    total_et = 0
    total_precip = 0
    total_duracion = 0
    total_agua = 0
    alertas = []

    resumen_dias = []
    detalle_dia_a_dia = []
    consumo_agua_diario = []

    for detalle in detalles:
        et = detalle.et_diario if detalle.et_diario is not None else 0
        lluvia = detalle.precipitacion if detalle.precipitacion is not None else 0
        duracion = detalle.duracion_horas if detalle.duracion_horas is not None else 0
        agua = detalle.cantidad_agua if detalle.cantidad_agua is not None else 0

        total_et += et
        total_precip += lluvia
        total_duracion += duracion
        total_agua += agua

        consumo_agua_diario.append(agua)

        resumen_dias.append(
            f"Día {detalle.dia} ({detalle.fecha.strftime('%d/%m/%Y')}): "
            f"Riego comenzó a las {detalle.hora_inicio.strftime('%H:%M')} por {detalle.duracion_formateada()}, "
            f"aplicando {agua:.2f} galones. ET: {et:.2f} mm, Precipitación: {lluvia:.2f} mm."
        )

        detalle_dia_a_dia.append({
            "dia": detalle.dia,
            "fecha": detalle.fecha.strftime('%Y-%m-%d'),
            "hora_inicio": detalle.hora_inicio.strftime('%H:%M'),
            "duracion_horas": duracion,
            "cantidad_agua": agua,
            "et_diario": et,
            "precipitacion": lluvia
        })

    num_dias = detalles.count()
    et_prom = total_et / num_dias if num_dias else 0
    precip_prom = total_precip / num_dias if num_dias else 0
    duracion_prom = total_duracion / num_dias if num_dias else 0
    agua_prom = total_agua / num_dias if num_dias else 0

    etapa = cultivo.etapa_crecimiento
    tipo_cultivo = cultivo.tipo_cultivo
    kc = 0
    if etapa == 'plantula':
        kc = tipo_cultivo.coef_plantula
    elif etapa == 'crecimiento':
        kc = tipo_cultivo.coef_crecimiento
    elif etapa == 'madurez':
        kc = tipo_cultivo.coef_madurez

    if duracion_prom > 24:
        alertas.append("🚨 El sistema de riego está funcionando demasiadas horas por día. Es posible que el caudal de agua sea muy bajo o el área del cultivo sea muy grande.")
    if precip_prom == 0:
        alertas.append("💧 No ha llovido nada durante los días analizados. Toda el agua debe ser aportada por el riego.")
    if et_prom > 5 and precip_prom < 1:
        alertas.append("☀️ Hace mucho calor y no ha llovido. El cultivo podría necesitar más agua de lo normal.")

    return {
        "ubicacion": f"{cultivo.ubicacion.ciudad}, {cultivo.ubicacion.pais}",
        "tipo_cultivo": cultivo.tipo_cultivo.nombre,
        "etapa_crecimiento": cultivo.get_etapa_crecimiento_display(),
        "kc": kc,
        "fecha_inicio": detalles.first().fecha.strftime('%d/%m/%Y') if detalles.exists() else "Desconocida",
        "consumo_agua_promedio": f"{agua_prom:.2f}",
        "consumo_agua_diario": consumo_agua_diario,
        "lluvia_promedio_diaria": f"{precip_prom:.2f}",
        "horas_riego_promedio": f"{duracion_prom:.2f}",
        "alertas": alertas,
        "detalle_diario": detalle_dia_a_dia,
        "resumen": (
            f"📍 Ubicación: {cultivo.ubicacion.ciudad}, {cultivo.ubicacion.pais}\n"
            f"🌱 Cultivo: {cultivo.tipo_cultivo.nombre}, etapa: {cultivo.get_etapa_crecimiento_display()}\n"
            f"💧 Tipo de riego: {cultivo.tipo_riego.nombre}, flujo: {cultivo.tasa_flujo} galones/hora\n"
            f"📅 Cronograma desde: {detalles.first().fecha.strftime('%d/%m/%Y') if detalles.exists() else 'Desconocida'}\n"
            f"💧 Coeficiente Kc: {kc:.2f}\n\n"
            f"📊 Promedios diarios:\n"
            f" - Evapotranspiración: {et_prom:.2f} mm\n"
            f" - Precipitación: {precip_prom:.2f} mm\n"
            f" - Duración de riego: {duracion_prom:.2f} h\n"
            f" - Agua aplicada: {agua_prom:.2f} galones\n\n"
            f"🗓️ Detalle diario:\n" + "\n".join(resumen_dias) + "\n\n"
            f"⚠️ Alertas:\n" + ("\n".join(alertas) if alertas else "Sin alertas detectadas.")
        )
    }
