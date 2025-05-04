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

Uso de agua (galones) = (coeficiente de cultivo × ET - precipitación) × área

Donde:
- ET: Evapotranspiración (mm/día)
- Precipitación: Lluvia esperada (mm/día)
- Coeficiente de cultivo: Varía según el tipo de cultivo y etapa de crecimiento
- Área: Superficie de la zona de cultivo (m²)

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un nuevo Pull Request
