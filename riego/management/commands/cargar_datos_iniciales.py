from django.core.management.base import BaseCommand
from riego.models import TipoCultivo, TipoRiego

class Command(BaseCommand):
    help = 'Carga datos iniciales para la aplicación AiRiego'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')
        
        # Crear tipos de cultivo
        if TipoCultivo.objects.count() == 0:
            self.stdout.write('Creando tipos de cultivo...')
            tipos_cultivo = [
                {
                    'nombre': 'Maíz',
                    'descripcion': 'Cultivo de maíz',
                    'coef_plantula': 0.3,
                    'coef_adulto': 1.2,
                    'coef_anciano': 0.6,
                    'es_predefinido': True
                },
                {
                    'nombre': 'Tomate',
                    'descripcion': 'Cultivo de tomate',
                    'coef_plantula': 0.4,
                    'coef_adulto': 1.15,
                    'coef_anciano': 0.7,
                    'es_predefinido': True
                },
                {
                    'nombre': 'Alfalfa',
                    'descripcion': 'Cultivo de alfalfa',
                    'coef_plantula': 0.35,
                    'coef_adulto': 0.95,
                    'coef_anciano': 0.5,
                    'es_predefinido': True
                },
                {
                    'nombre': 'Frijol',
                    'descripcion': 'Cultivo de frijol',
                    'coef_plantula': 0.3,
                    'coef_adulto': 1.05,
                    'coef_anciano': 0.6,
                    'es_predefinido': True
                },
                {
                    'nombre': 'Trigo',
                    'descripcion': 'Cultivo de trigo',
                    'coef_plantula': 0.3,
                    'coef_adulto': 1.15,
                    'coef_anciano': 0.4,
                    'es_predefinido': True
                }
            ]
            
            for tipo in tipos_cultivo:
                TipoCultivo.objects.create(**tipo)
            
            self.stdout.write(self.style.SUCCESS(f'Se crearon {len(tipos_cultivo)} tipos de cultivo'))
        else:
            self.stdout.write('Ya existen tipos de cultivo en la base de datos')
        
        # Crear tipos de riego
        if TipoRiego.objects.count() == 0:
            self.stdout.write('Creando tipos de riego...')
            tipos_riego = [
                {
                    'nombre': 'superficial',
                    'eficiencia': 0.6
                },
                {
                    'nombre': 'aspersion',
                    'eficiencia': 0.75
                },
                {
                    'nombre': 'goteo',
                    'eficiencia': 0.9
                },
                {
                    'nombre': 'subterraneo',
                    'eficiencia': 0.95
                }
            ]
            
            for tipo in tipos_riego:
                TipoRiego.objects.create(**tipo)
            
            self.stdout.write(self.style.SUCCESS(f'Se crearon {len(tipos_riego)} tipos de riego'))
        else:
            self.stdout.write('Ya existen tipos de riego en la base de datos')
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente'))
