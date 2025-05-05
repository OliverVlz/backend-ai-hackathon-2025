# AiRiego - Backend

Backend para la aplicación AiRiego, desarrollado con Django y Django REST Framework. Esta aplicación ayuda a los agricultores a optimizar sus horarios de riego semanales y el uso del agua, permitiéndoles mapear sus campos e ingresar información específica para generar un horario de riego sostenible y eficiente.

## Características

- API RESTful para gestionar zonas de cultivo, tipos de cultivo y sistemas de riego
- Sistema de autenticación basado en JWT
- Cálculo de necesidades de agua basado en evapotranspiración, precipitación y coeficientes de cultivo
- Generación de cronogramas de riego para 7 días

## Tecnologías utilizadas

- Django 5.2
- Django REST Framework
- Simple JWT para autenticación
- SQLite (por defecto)

## Requisitos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)

## Instalación y configuración

### Opción 1: Instalación con Docker

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/backend-ai-hackathon-2025.git
   cd backend-ai-hackathon-2025
   ```

2. Construir y ejecutar los contenedores con Docker Compose:
   ```bash
   docker-compose up --build
   ```

### Opción 2: Instalación local

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/backend-ai-hackathon-2025.git
   cd backend-ai-hackathon-2025
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```

5. Cargar datos iniciales:
   ```bash
   python manage.py cargar_datos_iniciales
   ```

6. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Estructura del proyecto

- `backend/`: Configuración principal del proyecto Django
- `riego/`: Aplicación principal que contiene los modelos, vistas y serializers
  - `models.py`: Definición de modelos (TipoCultivo, TipoRiego, ZonaCultivo, etc.)
  - `views.py`: Vistas y ViewSets para la API
  - `serializers.py`: Serializers para convertir modelos a JSON y viceversa
  - `urls.py`: Configuración de rutas de la API
  - `management/commands/`: Comandos personalizados, incluyendo `cargar_datos_iniciales`
  - `fixtures/`: Datos iniciales en formato JSON

## API Endpoints

- `/api/registro/`: Registro de usuarios
- `/api/token/`: Obtener tokens JWT
- `/api/token/refresh/`: Refrescar token JWT
- `/api/perfil/`: Obtener perfil del usuario autenticado
- `/api/tipos-cultivo/`: Listar y crear tipos de cultivo
- `/api/tipos-riego/`: Listar y crear tipos de riego
- `/api/zonas-cultivo/`: Listar y crear zonas de cultivo

## Fórmula para calcular el uso de agua

Uso de agua (galones) = max\[0, ((coeficiente de cultivo × ET - precipitación) × área) / (eficiencia × 3.785)]

**Donde:**
- **ET:** Evapotranspiración (mm/día)
- **Precipitación:** Lluvia esperada (mm/día)
- **Coeficiente de cultivo (Kc):** Varía según el tipo de cultivo y etapa de crecimiento
- **Área:** Superficie de la zona de cultivo (m²)
- **Eficiencia:** Eficiencia del sistema de riego (valor decimal, por ejemplo, 0.75 para 75%)
- **3.785:** Conversión de litros a galones (1 galón ≈ 3.785 litros)

**Notas importantes:**
- 1 mm de agua sobre 1 m² equivale a 1 litro de agua.
- Si la precipitación es mayor que la necesidad de agua, el resultado será 0 (no se recomienda riego ese día).
- La eficiencia del sistema de riego es fundamental para calcular la cantidad real de agua que debe aplicarse.

**Fórmula final recomendada:**

```
Uso de agua (galones) = max\[0, ((Kc × ET - Precipitación) × Área) / (Eficiencia × 3.785)]
```

## Lógica y fórmulas para el cálculo del cronograma de riego semanal

### 1. Datos necesarios
Para cada campo de cultivo se requieren:
- Coordenadas del polígono del campo (para calcular el área)
- Tipo de cultivo y etapa de crecimiento (para obtener el coeficiente de cultivo Kc)
- Eficiencia del sistema de riego y caudal (flow rate)
- Datos climáticos diarios para los próximos 7 días:
  - Evapotranspiración (ET) diaria (por ejemplo, de OpenET)
  - Precipitación diaria (por ejemplo, de Open-Meteo)

### 2. Cálculo del área del campo
- Se utiliza el Teorema del Zapatero (Shoelace Theorem) para calcular el área del polígono definido por las coordenadas.
- Para mayor precisión, se recomienda convertir las coordenadas geográficas a metros cuadrados considerando la curvatura de la Tierra (usando librerías como Turf.js en el frontend o GEOS/GeoDjango en el backend).

### 3. Obtención del coeficiente de cultivo (Kc)
- El coeficiente depende del tipo de cultivo y su etapa de crecimiento (plántula, adulto, envejecido).
- Este valor ajusta la ET de referencia a la necesidad real del cultivo.

### 4. Cálculo diario de la necesidad de agua
Para cada uno de los 7 días:
- **Fórmula:**
  ```
  Agua necesaria (mm) = (Kc × ETref) - Precipitación
  ```
- Si la precipitación es mayor que la necesidad, el resultado puede ser 0 (no se riega ese día).

#### Conversión a volumen:
- ```
  Volumen (litros) = max(0, Agua necesaria (mm) × Área (m²))
  ```
- 1 mm de agua sobre 1 m² = 1 litro.

#### Conversión a galones (opcional):
- ```
  Volumen (galones) = Volumen (litros) ÷ 3.785
  ```

### 5. Cálculo del tiempo de riego
Usando el caudal del sistema de riego (litros/hora o galones/hora) y la eficiencia:
- ```
  Horas de riego = Volumen total de agua requerido / (Caudal del sistema × Eficiencia)
  ```
- Si el caudal está en galones/hora y el volumen en galones, no es necesario convertir unidades.
- Se recomienda programar el riego a las 10 PM para minimizar la evaporación.

### 6. Generación del cronograma
Para cada día, el sistema muestra:
- Volumen de agua a aplicar
- Horario sugerido de riego
- Tiempo estimado de funcionamiento del sistema
- Datos climáticos usados para ese día

### 7. Ejemplo práctico
Supón que tienes:
- Área: 10,000 m²
- Kc: 0.8
- ETref (día 1): 5 mm
- Precipitación (día 1): 1 mm
- Caudal: 2,000 litros/hora
- Eficiencia: 0.75 (75%)

**Cálculo:**
- Agua necesaria = (0.8 × 5) - 1 = 3 mm
- Volumen = 3 mm × 10,000 m² = 30,000 litros
- Horas de riego = 30,000 / (2,000 × 0.75) = 20 horas

Esto se repite para cada uno de los 7 días, usando los datos climáticos diarios.

### 8. Recomendaciones y buenas prácticas
- Validar que ningún valor sea negativo (agua, horas, etc.).
- Si la precipitación es mayor que la necesidad, el riego debe ser 0 ese día.
- Automatizar la obtención de datos climáticos si es posible.
- Guardar el historial de cronogramas y los datos usados para trazabilidad y análisis.

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un nuevo Pull Request
