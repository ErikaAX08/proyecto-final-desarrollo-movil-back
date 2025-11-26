# 🎓 App Móvil Escolar - Backend API

Backend desarrollado con **Django REST Framework** para el sistema de gestión escolar. Proporciona APIs RESTful para la administración de usuarios (Administradores, Maestros y Alumnos).

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración de Base de Datos](#-configuración-de-base-de-datos)
- [Ejecución del Servidor](#-ejecución-del-servidor)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Pruebas en Postman](#-pruebas-en-postman)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

- ✅ **CRUD completo** para Administradores, Maestros y Alumnos
- ✅ **Autenticación** mediante Token Bearer
- ✅ **Validación de datos** en todas las operaciones
- ✅ **Relaciones** entre modelos (User ↔ Perfiles)
- ✅ **Eliminación en cascada** al borrar usuarios
- ✅ **CORS habilitado** para comunicación con el Frontend

---

## 🛠 Tecnologías

| Tecnología | Versión |
|------------|---------|
| Python | 3.10+ |
| Django | 5.0.2 |
| Django REST Framework | 3.16.1 |
| MySQL/MariaDB | 8.0+ |
| PyMySQL | Latest |

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.10 o superior**
   ```bash
   python --version
   # o
   python3 --version
   ```

2. **pip** (gestor de paquetes de Python)
   ```bash
   pip --version
   ```

3. **MySQL/MariaDB** instalado y corriendo
   ```bash
   mysql --version
   ```

4. **Virtualenv** (recomendado)
   ```bash
   pip install virtualenv
   ```

---

## 🚀 Instalación

### Paso 1: Clonar o navegar al proyecto

```bash
cd Backend
```

### Paso 2: Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄 Configuración de Base de Datos

### Paso 1: Crear la base de datos en MySQL

```sql
-- Conectarse a MySQL
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE app_movil_escolar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario (opcional)
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON app_movil_escolar.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### Paso 2: Configurar credenciales

Edita el archivo `app_movil_escolar_api/settings.py` y configura la sección de DATABASES:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_movil_escolar',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Paso 3: Ejecutar migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### Paso 4: Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

---

## ▶️ Ejecución del Servidor

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000/
```

Para especificar un puerto diferente:
```bash
python manage.py runserver 8080
```

---

## 📡 Endpoints de la API

### Base URL
```
http://127.0.0.1:8000/
```

### 🔐 Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/login/` | Iniciar sesión | ❌ |
| GET | `/logout/` | Cerrar sesión | ✅ |

### 👨‍💼 Administradores

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/lista-admins/` | Listar todos los administradores | ✅ |
| GET | `/admin/?id={id}` | Obtener administrador por ID | ✅ |
| POST | `/admin/` | Crear nuevo administrador | ❌ |
| PUT | `/admin/` | Actualizar administrador | ✅ |
| DELETE | `/admin/?id={id}` | Eliminar administrador | ✅ |

### 👨‍🏫 Maestros

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/lista-maestros/` | Listar todos los maestros | ✅ |
| GET | `/maestros/?id={id}` | Obtener maestro por ID | ✅ |
| POST | `/maestros/` | Crear nuevo maestro | ❌ |
| PUT | `/maestros/` | Actualizar maestro | ✅ |
| DELETE | `/maestros/?id={id}` | Eliminar maestro | ✅ |

### 👨‍🎓 Alumnos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/lista-alumnos/` | Listar todos los alumnos | ✅ |
| GET | `/alumnos/?id={id}` | Obtener alumno por ID | ✅ |
| POST | `/alumnos/` | Crear nuevo alumno | ❌ |
| PUT | `/alumnos/` | Actualizar alumno | ✅ |
| DELETE | `/alumnos/?id={id}` | Eliminar alumno | ✅ |

### 📊 Estadísticas

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/total-usuarios/` | Total de usuarios por rol | ❌ |

---

## 🧪 Pruebas en Postman

### Configuración Inicial

1. **Descargar e instalar Postman**: https://www.postman.com/downloads/
2. **Crear una nueva colección** llamada "App Móvil Escolar API"
3. **Configurar variable de entorno**:
   - Crear un Environment llamado "Local"
   - Agregar variable: `base_url` = `http://127.0.0.1:8000`

---

### 🔐 1. Login (Obtener Token)

**Request:**
```
POST {{base_url}}/login/
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "username": "admin@ejemplo.com",
    "password": "tu_password"
}
```

**Response esperada (200 OK):**
```json
{
    "token": "abc123xyz789...",
    "user": {
        "id": 1,
        "email": "admin@ejemplo.com",
        "first_name": "Admin",
        "last_name": "Principal"
    },
    "rol": "administrador"
}
```

> ⚠️ **IMPORTANTE**: Guarda el token para usarlo en las siguientes peticiones.

---

### 👨‍💼 2. CRUD de Administradores

#### 2.1 Crear Administrador (POST)

**Request:**
```
POST {{base_url}}/admin/
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "rol": "administrador",
    "clave_admin": "ADM001",
    "first_name": "Juan",
    "last_name": "Pérez García",
    "email": "juan.perez@escuela.edu.mx",
    "password": "Password123!",
    "telefono": "2221234567",
    "rfc": "PEGJ900101ABC",
    "edad": 35,
    "ocupacion": "Director Académico"
}
```

**Response esperada (201 Created):**
```json
{
    "admin_created_id": 1
}
```

#### 2.2 Listar Administradores (GET)

**Request:**
```
GET {{base_url}}/lista-admins/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Response esperada (200 OK):**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "first_name": "Juan",
            "last_name": "Pérez García",
            "email": "juan.perez@escuela.edu.mx"
        },
        "clave_admin": "ADM001",
        "telefono": "2221234567",
        "rfc": "PEGJ900101ABC",
        "edad": 35,
        "ocupacion": "Director Académico",
        "creation": "2025-11-25T10:30:00Z",
        "update": null
    }
]
```

#### 2.3 Obtener Administrador por ID (GET)

**Request:**
```
GET {{base_url}}/admin/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Response esperada (200 OK):**
```json
{
    "id": 1,
    "user": {
        "id": 1,
        "first_name": "Juan",
        "last_name": "Pérez García",
        "email": "juan.perez@escuela.edu.mx"
    },
    "clave_admin": "ADM001",
    "telefono": "2221234567",
    "rfc": "PEGJ900101ABC",
    "edad": 35,
    "ocupacion": "Director Académico"
}
```

#### 2.4 Actualizar Administrador (PUT)

**Request:**
```
PUT {{base_url}}/admin/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Body (raw JSON):**
```json
{
    "id": 1,
    "clave_admin": "ADM001",
    "first_name": "Juan Carlos",
    "last_name": "Pérez García",
    "telefono": "2229876543",
    "rfc": "PEGJ900101ABC",
    "edad": 36,
    "ocupacion": "Director General"
}
```

**Response esperada (200 OK):**
```json
{
    "message": "Administrador actualizado correctamente",
    "admin": {
        "id": 1,
        "user": {...},
        "clave_admin": "ADM001",
        ...
    }
}
```

#### 2.5 Eliminar Administrador (DELETE)

**Request:**
```
DELETE {{base_url}}/admin/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Response esperada (200 OK):**
```json
{
    "message": "Administrador eliminado correctamente"
}
```

---

### 👨‍🏫 3. CRUD de Maestros

#### 3.1 Crear Maestro (POST)

**Request:**
```
POST {{base_url}}/maestros/
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "rol": "maestro",
    "id_trabajador": "MTR001",
    "first_name": "María",
    "last_name": "González López",
    "email": "maria.gonzalez@escuela.edu.mx",
    "password": "Password123!",
    "fecha_nacimiento": "1985-05-15",
    "telefono": "2223456789",
    "rfc": "GOLM850515XYZ",
    "cubiculo": "A-101",
    "area_investigacion": "Desarrollo Web",
    "materias_json": ["Aplicaciones Web", "Programación 1", "Bases de datos"]
}
```

**Response esperada (201 Created):**
```json
{
    "Maestro creado con ID= ": 1
}
```

#### 3.2 Listar Maestros (GET)

**Request:**
```
GET {{base_url}}/lista-maestros/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

#### 3.3 Obtener Maestro por ID (GET)

**Request:**
```
GET {{base_url}}/maestros/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

#### 3.4 Actualizar Maestro (PUT)

**Request:**
```
PUT {{base_url}}/maestros/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Body (raw JSON):**
```json
{
    "id": 1,
    "id_trabajador": "MTR001",
    "first_name": "María Elena",
    "last_name": "González López",
    "fecha_nacimiento": "1985-05-15",
    "telefono": "2229999999",
    "rfc": "GOLM850515XYZ",
    "cubiculo": "B-202",
    "area_investigacion": "Programación",
    "materias_json": ["Desarrollo móvil", "Estructuras de datos"]
}
```

**Response esperada (200 OK):**
```json
{
    "message": "Maestro actualizado correctamente",
    "maestro": {...}
}
```

#### 3.5 Eliminar Maestro (DELETE)

**Request:**
```
DELETE {{base_url}}/maestros/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Response esperada (200 OK):**
```json
{
    "details": "Maestro eliminado"
}
```

---

### 👨‍🎓 4. CRUD de Alumnos

#### 4.1 Crear Alumno (POST)

**Request:**
```
POST {{base_url}}/alumnos/
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "rol": "alumno",
    "matricula": "202512345",
    "first_name": "Carlos",
    "last_name": "Ramírez Sánchez",
    "email": "carlos.ramirez@alumno.escuela.edu.mx",
    "password": "Password123!",
    "fecha_nacimiento": "2000-08-20",
    "curp": "RASC000820HPLMRR09",
    "rfc": "RASC000820ABC",
    "edad": 25,
    "telefono": "2227654321",
    "ocupacion": "Estudiante"
}
```

**Response esperada (201 Created):**
```json
{
    "Alumno creado con ID= ": 1
}
```

#### 4.2 Listar Alumnos (GET)

**Request:**
```
GET {{base_url}}/lista-alumnos/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

#### 4.3 Obtener Alumno por ID (GET)

**Request:**
```
GET {{base_url}}/alumnos/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

#### 4.4 Actualizar Alumno (PUT)

**Request:**
```
PUT {{base_url}}/alumnos/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Body (raw JSON):**
```json
{
    "id": 1,
    "matricula": "202512345",
    "first_name": "Carlos Alberto",
    "last_name": "Ramírez Sánchez",
    "fecha_nacimiento": "2000-08-20",
    "curp": "RASC000820HPLMRR09",
    "rfc": "RASC000820ABC",
    "edad": 25,
    "telefono": "2221111111",
    "ocupacion": "Estudiante de Ingeniería"
}
```

**Response esperada (200 OK):**
```json
{
    "message": "Alumno actualizado correctamente",
    "alumno": {...}
}
```

#### 4.5 Eliminar Alumno (DELETE)

**Request:**
```
DELETE {{base_url}}/alumnos/?id=1
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {tu_token_aquí}
```

**Response esperada (200 OK):**
```json
{
    "message": "Alumno eliminado correctamente"
}
```

---

### 📊 5. Estadísticas

#### Obtener Total de Usuarios

**Request:**
```
GET {{base_url}}/total-usuarios/
```

**Response esperada (200 OK):**
```json
{
    "admins": 5,
    "maestros": 12,
    "alumnos": 150
}
```

---

## 📁 Estructura del Proyecto

```
Backend/
├── app_movil_escolar_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py              # Modelos: Administradores, Maestros, Alumnos
│   ├── serializers.py         # Serializadores para la API
│   ├── settings.py            # Configuración de Django
│   ├── urls.py                # Rutas de la API
│   ├── views/
│   │   ├── __init__.py
│   │   ├── users.py           # Vistas de Administradores
│   │   ├── maestros.py        # Vistas de Maestros
│   │   ├── alumnos.py         # Vistas de Alumnos
│   │   ├── auth.py            # Vistas de Autenticación
│   │   └── bootstrap.py
│   └── migrations/            # Migraciones de BD
├── static/                    # Archivos estáticos
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'pymysql'"
```bash
pip install pymysql
```

### Error: "Access denied for user"
Verifica las credenciales en `settings.py` y que el usuario tenga permisos en MySQL.

### Error: "CORS blocked"
Asegúrate de que el frontend esté en `CORS_ALLOWED_ORIGINS` en `settings.py`.

### Error: "Token invalid or expired"
Vuelve a hacer login para obtener un nuevo token.

---

## 👥 Autores

- Desarrollo Web - Séptimo Semestre
- Universidad

---

## 📄 Licencia

Este proyecto es para fines educativos.
