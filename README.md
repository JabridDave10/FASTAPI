# Sistema de Citas Médicas - API REST

Una API REST completa para la gestión de citas médicas, pacientes, doctores y especialidades desarrollada con FastAPI y MySQL.

## 🚀 Características

- **Gestión completa de pacientes**: CRUD para información de pacientes
- **Gestión de especialidades médicas**: Administración de especialidades
- **Gestión de doctores**: CRUD para doctores con especialidades
- **Sistema de citas**: Agendar, modificar y cancelar citas
- **Historial médico**: Registro y consulta de historiales médicos
- **Verificación de disponibilidad**: Consulta de horarios disponibles por doctor y especialidad
- **API REST completa**: Endpoints para todas las operaciones CRUD
- **Documentación automática**: Swagger UI integrado

## 📋 Requisitos

- Python 3.8+
- MySQL 8.0+
- mysql-connector-python

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone <url-del-repositorio>
cd sistema-citas-medicas
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**:
   - Crear una base de datos MySQL llamada `sistema_citas`
   - Ejecutar el script SQL proporcionado en `database_schema.sql`
   - Actualizar la configuración en `database.py` con tus credenciales

5. **Ejecutar la aplicación**:
```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`
La documentación automática en: `http://localhost:8000/docs`

## 🗄️ Estructura de la Base de Datos

### Tablas principales:

- **paciente**: Información de pacientes
- **especialidad**: Especialidades médicas
- **doctor**: Doctores con sus especialidades
- **cita**: Citas médicas programadas
- **historial**: Historial médico de pacientes

## 📚 Endpoints de la API

### Pacientes
- `POST /pacientes/` - Crear paciente
- `GET /pacientes/` - Obtener todos los pacientes
- `GET /pacientes/{id}` - Obtener paciente específico
- `PUT /pacientes/{id}` - Actualizar paciente
- `DELETE /pacientes/{id}` - Eliminar paciente

### Especialidades
- `POST /especialidades/` - Crear especialidad
- `GET /especialidades/` - Obtener todas las especialidades
- `GET /especialidades/{id}` - Obtener especialidad específica
- `PUT /especialidades/{id}` - Actualizar especialidad
- `DELETE /especialidades/{id}` - Eliminar especialidad

### Doctores
- `POST /doctores/` - Crear doctor
- `GET /doctores/` - Obtener todos los doctores
- `GET /doctores/{id}` - Obtener doctor específico
- `GET /doctores/especialidad/{id}` - Obtener doctores por especialidad
- `PUT /doctores/{id}` - Actualizar doctor
- `DELETE /doctores/{id}` - Eliminar doctor

### Citas
- `POST /citas/` - Crear cita
- `GET /citas/` - Obtener todas las citas
- `GET /citas/{id}` - Obtener cita específica
- `GET /citas/paciente/{id}` - Obtener citas de un paciente
- `GET /citas/doctor/{id}` - Obtener citas de un doctor
- `PUT /citas/{id}` - Actualizar cita
- `DELETE /citas/{id}` - Cancelar cita

### Historial Médico
- `POST /historial/` - Crear registro de historial
- `GET /historial/{id}` - Obtener registro específico
- `GET /historial/paciente/{id}` - Obtener historial de un paciente
- `PUT /historial/{id}` - Actualizar historial
- `DELETE /historial/{id}` - Eliminar historial

### Disponibilidad
- `GET /disponibilidad/` - Obtener horarios disponibles
- `GET /disponibilidad/verificar/` - Verificar disponibilidad específica

## 💡 Ejemplos de Uso

### Crear un paciente
```bash
curl -X POST "http://localhost:8000/pacientes/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Juan",
       "apellido": "Pérez",
       "fecha_nacimiento": "1990-05-15",
       "telefono": "3001234567",
       "email": "juan.perez@email.com",
       "direccion": "Calle 123 #45-67"
     }'
```

### Crear una especialidad
```bash
curl -X POST "http://localhost:8000/especialidades/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Cardiología",
       "descripcion": "Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del corazón"
     }'
```

### Crear un doctor
```bash
curl -X POST "http://localhost:8000/doctores/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "María",
       "apellido": "García",
       "telefono": "3009876543",
       "email": "maria.garcia@clinica.com",
       "id_especialidad": 1
     }'
```

### Agendar una cita
```bash
curl -X POST "http://localhost:8000/citas/" \
     -H "Content-Type: application/json" \
     -d '{
       "fecha_hora": "2024-01-15T10:00:00",
       "motivo": "Consulta de rutina",
       "id_paciente": 1,
       "id_doctor": 1
     }'
```

### Consultar disponibilidad
```bash
curl "http://localhost:8000/disponibilidad/?fecha=2024-01-15&id_especialidad=1"
```

## 🔧 Configuración de la Base de Datos

Actualiza el archivo `database.py` con tus credenciales de MySQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "tu_usuario",
    "password": "tu_password",
    "database": "sistema_citas"
}
```

## 📖 Documentación

La documentación interactiva de la API está disponible en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Pruebas

Para probar la API, puedes usar:
- La interfaz Swagger UI en `/docs`
- Herramientas como Postman o Insomnia
- curl desde la línea de comandos
- Los ejemplos proporcionados en este README

## 📝 Notas Importantes

- Asegúrate de que MySQL esté ejecutándose en el puerto 3306
- La base de datos debe estar creada antes de ejecutar la aplicación
- Los horarios disponibles están configurados de 8:00 AM a 6:00 PM con intervalos de 30 minutos
- Todas las fechas deben estar en formato ISO (YYYY-MM-DD)
- Las fechas y horas de las citas deben estar en formato ISO (YYYY-MM-DDTHH:MM:SS)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir mejoras.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
