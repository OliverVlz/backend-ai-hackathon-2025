import requests
from shapely.geometry import shape
def get_centroid_lat_lon(geojson):
    """
    Calcula el centroide de un GeoJSON y devuelve (latitud, longitud).
    """
    geom = shape(geojson)
    centroid = geom.centroid
    return centroid.y, centroid.x  # lat, lon
def obtener_datos_meteorologicos(lat, lon, days: int = 7):
    """
    Devuelve una lista de dicts con:
      - fecha:      'YYYY-MM-DD'
      - et0:        float (mm/día)
      - precipitacion: float (mm/día)
    """
    url = "https://api.open-meteo.com/v1/forecast"
    # Aquí el daily debe ir COMA-SEPARADO, no con dos claves 'daily'
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "et0_fao_evapotranspiration,precipitation_sum",
        "timezone": "America/Costa_Rica",
        "forecast_days": days
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json().get("daily", {})

    fechas = data.get("time", [])
    et0s   = data.get("et0_fao_evapotranspiration", [])
    lluvias= data.get("precipitation_sum", [])

    # Debug inmediato:  
    print("🎯 WEATHER_SERVICE - daily keys:", list(data.keys()))
    print("🎯 WEATHER_SERVICE - muestras:", 
          fechas[:2], et0s[:2], lluvias[:2])

    if not (len(fechas) == len(et0s) == len(lluvias)):
        raise ValueError("📌 Longitudes diarias inconsistentes")

    return [
        {"fecha": fechas[i],
         "et0":   float(et0s[i]),
         "precipitacion": float(lluvias[i])}
        for i in range(len(fechas))
    ]
