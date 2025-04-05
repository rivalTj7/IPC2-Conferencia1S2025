#!/usr/bin/env python
"""
Script para configurar un entorno de demostración con datos de ejemplo.
Ejecutar después de las migraciones iniciales: python scripts/setup_demo.py
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar entorno Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conference_manager.settings')
django.setup()

# Importar modelos después de configurar Django
from django.contrib.auth import get_user_model
from apps.users.models import CustomUser
from apps.events.models import Category, Location, Event, Session
from apps.speakers.models import Specialization, SpeakerProfile, Presentation
from apps.core.models import FAQ, Sponsor

def create_superuser():
    """Crear superusuario si no existe"""
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        print('✅ Superusuario creado: admin / adminpassword')
    else:
        print('ℹ️ El superusuario ya existe')

def create_users():
    """Crear usuarios de demostración"""
    users_data = [
        {
            'username': 'juan.perez',
            'email': 'juan@example.com',
            'password': 'password123',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'bio': 'Desarrollador full-stack con experiencia en Python y JavaScript.',
            'organization': 'Tecnologías Innovadoras',
            'job_title': 'Desarrollador Senior'
        },
        {
            'username': 'maria.lopez',
            'email': 'maria@example.com',
            'password': 'password123',
            'first_name': 'María',
            'last_name': 'López',
            'bio': 'Especialista en UI/UX y diseño de producto.',
            'organization': 'Diseño Creativo',
            'job_title': 'Diseñadora UX'
        },
        {
            'username': 'carlos.rodriguez',
            'email': 'carlos@example.com',
            'password': 'password123',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'bio': 'Experto en DevOps y arquitectura de software.',
            'organization': 'Cloud Solutions',
            'job_title': 'DevOps Engineer'
        },
        {
            'username': 'ana.martinez',
            'email': 'ana@example.com',
            'password': 'password123',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'bio': 'Especialista en ciberseguridad y protección de datos.',
            'organization': 'SecureTech',
            'job_title': 'Security Analyst'
        },
        {
            'username': 'roberto.sanchez',
            'email': 'roberto@example.com',
            'password': 'password123',
            'first_name': 'Roberto',
            'last_name': 'Sánchez',
            'bio': 'Ingeniero de datos con experiencia en big data y analítica.',
            'organization': 'DataMax',
            'job_title': 'Data Engineer'
        }
    ]
    
    created_count = 0
    for user_data in users_data:
        if not CustomUser.objects.filter(username=user_data['username']).exists():
            user = CustomUser.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                bio=user_data['bio'],
                organization=user_data['organization'],
                job_title=user_data['job_title']
            )
            created_count += 1
    
    print(f'✅ {created_count} usuarios de demostración creados')

def create_categories():
    """Crear categorías de eventos"""
    categories_data = [
        {'name': 'Desarrollo Web', 'slug': 'desarrollo-web', 'description': 'Eventos sobre desarrollo web, frontend y backend'},
        {'name': 'Inteligencia Artificial', 'slug': 'inteligencia-artificial', 'description': 'Eventos sobre IA, machine learning y data science'},
        {'name': 'DevOps', 'slug': 'devops', 'description': 'Eventos sobre DevOps, CI/CD y cloud computing'},
        {'name': 'Diseño UX/UI', 'slug': 'diseno-ux-ui', 'description': 'Eventos sobre diseño de experiencia de usuario e interfaces'},
        {'name': 'Mobile', 'slug': 'mobile', 'description': 'Eventos sobre desarrollo de aplicaciones móviles'},
        {'name': 'Seguridad', 'slug': 'seguridad', 'description': 'Eventos sobre ciberseguridad y protección de datos'}
    ]
    
    created_count = 0
    for cat_data in categories_data:
        if not Category.objects.filter(slug=cat_data['slug']).exists():
            Category.objects.create(**cat_data)
            created_count += 1
    
    print(f'✅ {created_count} categorías creadas')

def create_locations():
    """Crear ubicaciones de eventos"""
    locations_data = [
        {
            'name': 'Centro de Convenciones Tecnológico',
            'address': 'Av. Tecnología 123',
            'city': 'Ciudad de México',
            'state': 'CDMX',
            'country': 'México',
            'capacity': 1000
        },
        {
            'name': 'Hotel Business Plaza',
            'address': 'Calle Negocios 456',
            'city': 'Guadalajara',
            'state': 'Jalisco',
            'country': 'México',
            'capacity': 500
        },
        {
            'name': 'Campus Universitario Digital',
            'address': 'Blvd. Educación 789',
            'city': 'Monterrey',
            'state': 'Nuevo León',
            'country': 'México',
            'capacity': 800
        },
        {
            'name': 'Hub de Innovación',
            'address': 'Av. Emprendedores 234',
            'city': 'Querétaro',
            'state': 'Querétaro',
            'country': 'México',
            'capacity': 300
        }
    ]
    
    created_count = 0
    for loc_data in locations_data:
        if not Location.objects.filter(name=loc_data['name'], city=loc_data['city']).exists():
            Location.objects.create(**loc_data)
            created_count += 1
    
    print(f'✅ {created_count} ubicaciones creadas')

def create_specializations():
    """Crear especializaciones de ponentes"""
    specializations_data = [
        {'name': 'Frontend', 'slug': 'frontend', 'description': 'Especialización en tecnologías frontend'},
        {'name': 'Backend', 'slug': 'backend', 'description': 'Especialización en tecnologías backend'},
        {'name': 'DevOps', 'slug': 'devops', 'description': 'Especialización en DevOps y CI/CD'},
        {'name': 'UX/UI', 'slug': 'ux-ui', 'description': 'Especialización en diseño de experiencia de usuario'},
        {'name': 'Mobile', 'slug': 'mobile', 'description': 'Especialización en desarrollo móvil'},
        {'name': 'Data Science', 'slug': 'data-science', 'description': 'Especialización en ciencia de datos'},
        {'name': 'Cloud', 'slug': 'cloud', 'description': 'Especialización en cloud computing'},
        {'name': 'Seguridad', 'slug': 'seguridad', 'description': 'Especialización en ciberseguridad'}
    ]
    
    created_count = 0
    for spec_data in specializations_data:
        if not Specialization.objects.filter(slug=spec_data['slug']).exists():
            Specialization.objects.create(**spec_data)
            created_count += 1
    
    print(f'✅ {created_count} especializaciones creadas')

def create_speaker_profiles():
    """Crear perfiles de ponentes"""
    # Hacer que algunos usuarios existentes sean ponentes
    users = CustomUser.objects.filter(is_superuser=False)[:3]
    specializations = Specialization.objects.all()
    
    created_count = 0
    for user in users:
        if not hasattr(user, 'speaker_profile'):
            # Marcar usuario como ponente
            user.is_speaker = True
            user.save()
            
            # Crear perfil de ponente
            speaker_profile = SpeakerProfile.objects.create(
                user=user,
                headline=f"Experto en {random.choice(['Desarrollo', 'Diseño', 'DevOps', 'Cloud', 'AI'])}",
                bio_extended=f"Perfil profesional extendido de {user.get_full_name()}. Con amplia experiencia en el sector tecnológico.",
                website=f"https://www.{user.username}.com",
                featured=random.choice([True, False]),
                speaking_experience="Ponente en diversas conferencias nacionales e internacionales.",
                languages="Español, Inglés",
                presentation_topics="Desarrollo web, Cloud computing, Inteligencia Artificial"
            )
            
            # Agregar especializaciones aleatorias
            random_specs = random.sample(list(specializations), k=random.randint(1, 3))
            speaker_profile.specializations.add(*random_specs)
            
            # Crear presentaciones pasadas
            for i in range(1, 4):
                days_ago = random.randint(30, 365)
                presentation_date = timezone.now() - timedelta(days=days_ago)
                
                Presentation.objects.create(
                    speaker=speaker_profile,
                    title=f"Presentación {i} de {user.get_full_name()}",
                    event_name=f"Conferencia Tech {2023 - (i % 3)}",
                    date=presentation_date,
                    description=f"Descripción de la presentación {i} de {user.get_full_name()}"
                )
            
            created_count += 1
    
    print(f'✅ {created_count} perfiles de ponentes creados')

def create_events():
    """Crear eventos de demostración"""
    categories = Category.objects.all()
    locations = Location.objects.all()
    organizer = CustomUser.objects.filter(is_superuser=True).first()
    speakers = CustomUser.objects.filter(is_speaker=True)
    
    events_data = [
        {
            'title': 'Conferencia de Desarrollo Web 2025',
            'slug': 'conferencia-desarrollo-web-2025',
            'description': 'La conferencia más importante sobre desarrollo web en Latinoamérica. Aprende las últimas tecnologías y tendencias en frontend y backend.',
            'start_date': timezone.now() + timedelta(days=30),
            'end_date': timezone.now() + timedelta(days=32),
            'status': Event.EventStatus.PUBLISHED,
            'registration_required': True,
            'max_attendees': 500,
            'is_featured': True
        },
        {
            'title': 'Workshop de Django Avanzado',
            'slug': 'workshop-django-avanzado',
            'description': 'Workshop intensivo de Django. Aprende a construir aplicaciones web robustas y escalables con Django y Django REST Framework.',
            'start_date': timezone.now() + timedelta(days=15),
            'end_date': timezone.now() + timedelta(days=15, hours=8),
            'status': Event.EventStatus.PUBLISHED,
            'registration_required': True,
            'max_attendees': 100,
            'is_featured': False
        },
        {
            'title': 'DevOps Summit 2025',
            'slug': 'devops-summit-2025',
            'description': 'Conferencia dedicada a las mejores prácticas de DevOps, CI/CD, y despliegue en la nube.',
            'start_date': timezone.now() + timedelta(days=60),
            'end_date': timezone.now() + timedelta(days=61),
            'status': Event.EventStatus.PUBLISHED,
            'registration_required': True,
            'max_attendees': 300,
            'is_featured': True
        },
        {
            'title': 'Hackathon IA para Todos',
            'slug': 'hackathon-ia-para-todos',
            'description': 'Un fin de semana para desarrollar soluciones innovadoras utilizando inteligencia artificial.',
            'start_date': timezone.now() + timedelta(days=45),
            'end_date': timezone.now() + timedelta(days=47),
            'status': Event.EventStatus.PUBLISHED,
            'registration_required': True,
            'max_attendees': 200,
            'is_featured': False
        }
    ]
    
    created_count = 0
    session_count = 0
    
    for event_data in events_data:
        if not Event.objects.filter(slug=event_data['slug']).exists():
            # Asignar categoría y ubicación aleatorias
            event_data['category'] = random.choice(categories)
            event_data['location'] = random.choice(locations)
            event_data['organizer'] = organizer
            
            # Crear evento
            event = Event.objects.create(**event_data)
            created_count += 1
            
            # Crear sesiones para el evento
            event_duration = (event.end_date - event.start_date).days
            for day in range(event_duration + 1):
                for hour in range(10, 17, 2):  # Sesiones a las 10, 12, 14, 16
                    session_date = event.start_date + timedelta(days=day)
                    session_start = session_date.replace(hour=hour, minute=0, second=0)
                    session_end = session_date.replace(hour=hour+1, minute=30, second=0)
                    
                    if session_start < event.end_date:
                        session = Session.objects.create(
                            title=f"Sesión {day+1}.{hour//2}: {random.choice(['Introducción', 'Taller', 'Panel', 'Keynote'])}",
                            description=f"Descripción de la sesión para el día {day+1} a las {hour}:00",
                            event=event,
                            start_time=session_start,
                            end_time=session_end,
                            room=f"Sala {random.randint(1, 5)}"
                        )
                        
                        # Asignar ponentes aleatorios a la sesión
                        random_speakers = random.sample(list(speakers), k=random.randint(1, min(3, speakers.count())))
                        session.speakers.add(*random_speakers)
                        
                        session_count += 1
    
    print(f'✅ {created_count} eventos creados con {session_count} sesiones')

def create_faqs():
    """Crear preguntas frecuentes"""
    faqs_data = [
        {
            'question': '¿Cómo me registro para un evento?',
            'answer': 'Para registrarte, navega a la página del evento que te interesa y haz clic en el botón "Registrarse". Necesitarás tener una cuenta en nuestra plataforma para completar el registro.',
            'order': 1
        },
        {
            'question': '¿Puedo cancelar mi registro a un evento?',
            'answer': 'Sí, puedes cancelar tu registro hasta 48 horas antes del inicio del evento. Para hacerlo, ve a "Mi Perfil" > "Mis Inscripciones" y selecciona la opción de cancelar para el evento correspondiente.',
            'order': 2
        },
        {
            'question': '¿Cómo puedo convertirme en ponente?',
            'answer': 'Para ser ponente, debes crear una cuenta y luego completar tu perfil de ponente con tu experiencia y especialidades. Una vez hecho esto, puedes solicitar participar como ponente en eventos futuros.',
            'order': 3
        },
        {
            'question': '¿Los eventos tienen algún costo?',
            'answer': 'Algunos eventos son gratuitos y otros tienen un costo. La información sobre el precio se indica claramente en la página de cada evento.',
            'order': 4
        },
        {
            'question': '¿Recibo algún certificado por asistir?',
            'answer': 'Sí, para la mayoría de los eventos proporcionamos certificados de asistencia que podrás descargar desde tu perfil después de que el evento haya finalizado.',
            'order': 5
        }
    ]
    
    created_count = 0
    for faq_data in faqs_data:
        if not FAQ.objects.filter(question=faq_data['question']).exists():
            FAQ.objects.create(**faq_data)
            created_count += 1
    
    print(f'✅ {created_count} preguntas frecuentes creadas')

def create_sponsors():
    """Crear patrocinadores de ejemplo"""
    sponsors_data = [
        {
            'name': 'TechCorp',
            'description': 'Empresa líder en soluciones tecnológicas empresariales.',
            'level': Sponsor.SponsorLevel.PLATINUM,
            'website': 'https://www.techcorp-example.com',
            'active': True
        },
        {
            'name': 'DataSoft',
            'description': 'Especialistas en soluciones de big data y análisis.',
            'level': Sponsor.SponsorLevel.GOLD,
            'website': 'https://www.datasoft-example.com',
            'active': True
        },
        {
            'name': 'CloudNet',
            'description': 'Proveedor de servicios de cloud computing y redes.',
            'level': Sponsor.SponsorLevel.GOLD,
            'website': 'https://www.cloudnet-example.com',
            'active': True
        },
        {
            'name': 'DevTools',
            'description': 'Herramientas para desarrolladores y equipos de tecnología.',
            'level': Sponsor.SponsorLevel.SILVER,
            'website': 'https://www.devtools-example.com',
            'active': True
        },
        {
            'name': 'StartupHub',
            'description': 'Aceleradora de startups tecnológicas.',
            'level': Sponsor.SponsorLevel.BRONZE,
            'website': 'https://www.startuphub-example.com',
            'active': True
        }
    ]
    
    created_count = 0
    for sponsor_data in sponsors_data:
        if not Sponsor.objects.filter(name=sponsor_data['name']).exists():
            # Nota: En un caso real, aquí se añadiría un logo
            Sponsor.objects.create(**sponsor_data)
            created_count += 1
    
    print(f'✅ {created_count} patrocinadores creados')

def main():
    """Función principal para configurar datos de demostración"""
    print("\n🚀 Configurando entorno de demostración...\n")
    
    create_superuser()
    create_users()
    create_categories()
    create_locations()
    create_specializations()
    create_speaker_profiles()
    create_events()
    create_faqs()
    create_sponsors()
    
    print("\n✨ ¡Entorno de demostración configurado con éxito! ✨\n")
    print("Puedes iniciar sesión como administrador con:")
    print("  Username: admin")
    print("  Password: adminpassword")
    print("\nO usar cualquiera de los usuarios de demostración:")
    print("  Username: juan.perez, maria.lopez, etc.")
    print("  Password: password123")

if __name__ == '__main__':
    main()