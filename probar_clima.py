import sys
import os

# Añade la raíz del proyecto al path para importar el paquete `riego`
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from riego.services.weather_service import obtener_datos_meteorologicos


def main():
    # Coordenadas de San José, Costa Rica
    lat, lon = 9.9281, -84.0907
    try:
        pronostico = obtener_datos_meteorologicos(lat, lon)
        print("Pronóstico diario (próximos 7 días):")
        for dia in pronostico:
            print(f"Fecha: {dia['fecha']} | ET0: {dia['et0']} mm | Precipitación: {dia['precipitacion']} mm")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()