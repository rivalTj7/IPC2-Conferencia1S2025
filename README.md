# Sistema de Gestión de Conferencias - Guía Local

Esta guía te ayudará a configurar y ejecutar el Sistema de Gestión de Conferencias en tu entorno local para propósitos de desarrollo y pruebas.

## Requisitos previos

- Python 3.8+ instalado en tu sistema
- Pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Configuración del entorno local

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/rivalTj7/IPC2-Conferencia1S2025
cd conference-manager
```

Si no estás usando git, simplemente descarga y descomprime el proyecto en tu directorio preferido.

### 2. Crear y activar un entorno virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (si no existe) con el siguiente contenido:

```
SECRET_KEY=django-insecure-esta-clave-es-solo-para-desarrollo-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos por defecto (SQLite)
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Aplicar migraciones de la base de datos

```bash
python manage.py migrate
```

### 6. Crear un superusuario

Para acceder al panel de administración y gestionar el sistema, necesitas crear un superusuario:

```bash
python manage.py createsuperuser
```

Sigue las indicaciones para ingresar un nombre de usuario, correo electrónico y contraseña.

### 7. Cargar datos de ejemplo (opcional)

Si quieres cargar datos de ejemplo para probar el sistema:

```bash
python scripts/setup_demo.py
```

### 8. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Ahora puedes acceder a la aplicación en tu navegador visitando: http://127.0.0.1:8000/

## Acceso al sistema

### Panel de administración

- URL: http://127.0.0.1:8000/admin/
- Usuario: *el nombre de usuario que creaste en el paso 6*
- Contraseña: *la contraseña que configuraste en el paso 6*

### Sitio público

- URL principal: http://127.0.0.1:8000/
- Registro de usuario: http://127.0.0.1:8000/usuarios/registro/
- Inicio de sesión: http://127.0.0.1:8000/usuarios/login/

## Estructura del proyecto

```
conference_manager/          # Directorio raíz del proyecto
│
├── conference_manager/      # Configuración principal
│   ├── settings.py          # Configuración del proyecto
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
│
├── apps/                    # Aplicaciones del proyecto
│   ├── core/                # Funcionalidad central
│   ├── events/              # Gestión de eventos
│   ├── speakers/            # Perfiles de ponentes
│   └── users/               # Gestión de usuarios
│
├── templates/               # Plantillas HTML
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── media/                   # Archivos subidos por usuarios
├── scripts/                 # Scripts útiles
│   └── setup_demo.py        # Script para cargar datos de ejemplo
│
├── manage.py                # Script de gestión de Django
├── requirements.txt         # Dependencias del proyecto
└── .env                     # Variables de entorno (crear manualmente)
```

## Guía rápida del sistema

### Módulos principales

1. **Eventos**
   - Listado de eventos
   - Detalles de eventos
   - Registro para eventos
   - Sesiones dentro de eventos

2. **Ponentes**
   - Listado de ponentes
   - Perfiles detallados
   - Historial de presentaciones

3. **Usuarios**
   - Registro e inicio de sesión
   - Perfiles de usuario
   - Gestión de inscripciones a eventos

### Panel de administración

El panel de administración de Django te permite:

1. **Gestionar usuarios**
   - Crear, editar y eliminar usuarios
   - Asignar permisos y roles

2. **Administrar eventos**
   - Crear nuevos eventos
   - Gestionar categorías y ubicaciones
   - Programar sesiones
   - Ver registros de asistentes

3. **Gestionar ponentes**
   - Aprobar perfiles de ponentes
   - Asignar especializaciones
   - Revisar presentaciones

## Solución de problemas comunes

### Error al ejecutar migraciones

Si encuentras errores al ejecutar las migraciones, intenta:

```bash
python manage.py migrate --run-syncdb
```

### Error de módulo no encontrado

Asegúrate de que estás en el directorio correcto y que el entorno virtual está activado:

```bash
# Verificar directorio
pwd  # en Unix/Linux/macOS
cd   # en Windows

# Activar entorno virtual nuevamente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/Linux/macOS
```

### Error con archivos estáticos o de media

Ejecuta el siguiente comando para recopilar archivos estáticos:

```bash
python manage.py collectstatic
```

### Reiniciar la base de datos (si es necesario)

Si necesitas reiniciar completamente la base de datos:

1. Elimina el archivo `db.sqlite3`
2. Elimina los archivos de migración (excepto `__init__.py`) en las carpetas `migrations` de cada aplicación
3. Ejecuta:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Contacto y soporte

Si tienes alguna pregunta o problema con la instalación:
- Email: rival.alex7@gmail.com
- GitHub: https://github.com/rivalTj7

---