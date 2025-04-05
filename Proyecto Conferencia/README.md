# Sistema de Gestión de Conferencias

Un sistema completo para la gestión de conferencias, desarrollado con Django. Este proyecto sirve como ejemplo para mostrar las mejores prácticas de desarrollo con Django.

## Características

- Gestión de usuarios con perfiles personalizados
- Registro y administración de eventos
- Perfiles de ponentes y gestión de presentaciones
- Sistema de registro para asistentes
- Área administrativa completa
- Diseño responsivo con Bootstrap 5

## Requisitos

- Python 3.8+
- Django 4.2+
- Otras dependencias listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/rivalTj7/IPC2-Conferencia1S2025
   cd conference-manager
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   - Copia el archivo `.env.example` a `.env` y edita los valores según sea necesario

5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

7. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

8. Visita http://127.0.0.1:8000/ en tu navegador

## Estructura del Proyecto

```
conference_manager/
│
├── apps/                       # Aplicaciones del proyecto
│   ├── core/                   # Funcionalidad central del sitio
│   ├── events/                 # Gestión de eventos
│   ├── speakers/               # Perfiles de ponentes
│   └── users/                  # Gestión de usuarios
│
├── conference_manager/         # Configuración principal del proyecto
│   ├── settings.py             # Configuración del proyecto
│   ├── urls.py                 # URLs principales
│   ├── asgi.py                 # Configuración ASGI
│   └── wsgi.py                 # Configuración WSGI
│
├── media/                      # Archivos subidos por usuarios
│
├── static/                     # Archivos estáticos
│   ├── css/                    # Hojas de estilo
│   ├── js/                     # JavaScript
│   └── img/                    # Imágenes
│
├── templates/                  # Plantillas HTML
│   ├── base/                   # Plantillas base
│   ├── core/                   # Plantillas de la app core
│   ├── events/                 # Plantillas de eventos
│   ├── speakers/               # Plantillas de ponentes
│   └── users/                  # Plantillas de usuarios
│
├── .env                        # Variables de entorno (no incluido en el repo)
├── .gitignore                  # Archivos ignorados por Git
├── manage.py                   # Script de gestión de Django
└── requirements.txt            # Dependencias del proyecto
```

## Despliegue

### Preparación para Producción

1. Actualiza las variables de entorno para producción en el archivo `.env`:
   - Establece `DEBUG=False`
   - Configura `ALLOWED_HOSTS` con los dominios de producción
   - Configura una base de datos PostgreSQL
   - Configura el correo electrónico SMTP

2. Recopila archivos estáticos:
   ```bash
   python manage.py collectstatic
   ```

### Despliegue en PythonAnywhere

1. Crea una cuenta en PythonAnywhere y configura un nuevo proyecto web

2. Configura un virtualenv en PythonAnywhere:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 myenv
   ```

3. Clona el repositorio:
   ```bash
   git clone https://github.com/rivalTj7/IPC2-Conferencia1S2025
   ```

4. Instala las dependencias:
   ```bash
   cd conference-manager
   pip install -r requirements.txt
   ```

5. Configura el archivo WSGI para PythonAnywhere (usando el asistente web)

6. Configura las variables de entorno en el archivo `.env`

7. Ejecuta las migraciones:
   ```bash
   python manage.py migrate
   ```

8. Recopila los archivos estáticos:
   ```bash
   python manage.py collectstatic
   ```

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Añadir una característica asombrosa'`)
4. Haz push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Rivaldo Alexander Tojín - rival.alex7@gmail.com

Link del proyecto: [https://github.com/rivalTj7/IPC2-Conferencia1S2025](https://github.com/rivalTj7/IPC2-Conferencia1S2025)