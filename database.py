import mysql.connector
from mysql.connector import Error
from typing import Optional
import os

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "maglev.proxy.rlwy.net"),
    "port": int(os.getenv("DB_PORT", 42337)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "IyiknVQqDZqjGGVpGAsgGLWkseIPZozY"),
    "database": os.getenv("DB_DATABASE", "railway")
}

def get_connection():
    """Obtiene una conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None

def execute_query(query: str, params: Optional[tuple] = None, fetch: bool = False):
    """Ejecuta una consulta SQL y retorna los resultados si es necesario"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
        
        cursor.close()
        return result
    except Error as e:
        print(f"Error ejecutando consulta: {e}")
        connection.rollback()
        return None
    finally:
        connection.close()

def execute_query_one(query: str, params: Optional[tuple] = None):
    """Ejecuta una consulta SQL y retorna un solo resultado"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result
    except Error as e:
        print(f"Error ejecutando consulta: {e}")
        return None
    finally:
        connection.close()

def initialize_database():
    """Inicializa la base de datos creando las tablas y datos de ejemplo"""
    print("🗄️  Inicializando base de datos...")
    
    # Crear base de datos si no existe
    config_without_db = DB_CONFIG.copy()
    del config_without_db['database']
    
    try:
        connection = mysql.connector.connect(**config_without_db)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        connection.close()
        print(f"✅ Base de datos '{DB_CONFIG['database']}' verificada")
    except Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False
    
    # Conectar a la base de datos específica
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Crear tablas
        tables_sql = [
            # Tabla Paciente
            """CREATE TABLE IF NOT EXISTS paciente (
                id_paciente INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                fecha_nacimiento DATE NOT NULL,
                telefono VARCHAR(20) UNIQUE,
                email VARCHAR(120) UNIQUE,
                direccion VARCHAR(200)
            )""",
            
            # Tabla Especialidad
            """CREATE TABLE IF NOT EXISTS especialidad (
                id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT
            )""",
            
            # Tabla Doctor
            """CREATE TABLE IF NOT EXISTS doctor (
                id_doctor INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                email VARCHAR(150) UNIQUE,
                id_especialidad INT NOT NULL,
                FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad)
            )""",
            
            # Tabla Historial
            """CREATE TABLE IF NOT EXISTS historial (
                id_historial INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                diagnostico TEXT,
                tratamiento TEXT,
                observaciones TEXT,
                id_paciente INT NOT NULL,
                id_doctor INT NOT NULL,
                FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
                FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor)
            )""",
            
            # Tabla Citas
            """CREATE TABLE IF NOT EXISTS cita (
                id_cita INT AUTO_INCREMENT PRIMARY KEY,
                fecha_hora DATETIME NOT NULL,
                motivo VARCHAR(255),
                id_paciente INT,
                id_doctor INT,
                FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
                FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor)
            )"""
        ]
        
        # Ejecutar creación de tablas
        for table_sql in tables_sql:
            try:
                cursor.execute(table_sql)
                connection.commit()
            except Error as e:
                if "already exists" not in str(e).lower():
                    print(f"⚠️  Advertencia creando tabla: {e}")
        
        print("✅ Tablas creadas/verificadas")
        
        # Verificar si ya existen datos de ejemplo
        cursor.execute("SELECT COUNT(*) as count FROM especialidad")
        result = cursor.fetchone()
        
        if result and result[0] == 0:
            print("📝 Insertando datos de ejemplo...")
            
            # Insertar especialidades de ejemplo
            especialidades = [
                ('Cardiología', 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del corazón'),
                ('Dermatología', 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de la piel'),
                ('Pediatría', 'Especialidad médica que se encarga del cuidado de la salud de los niños'),
                ('Ginecología', 'Especialidad médica que se encarga de la salud del sistema reproductor femenino'),
                ('Ortopedia', 'Especialidad médica que se encarga del diagnóstico y tratamiento de lesiones y enfermedades del sistema musculoesquelético')
            ]
            
            for especialidad in especialidades:
                cursor.execute("INSERT INTO especialidad (nombre, descripcion) VALUES (%s, %s)", especialidad)
            
            # Insertar doctores de ejemplo
            doctores = [
                ('María', 'García', '3001234567', 'maria.garcia@clinica.com', 1),
                ('Carlos', 'Rodríguez', '3002345678', 'carlos.rodriguez@clinica.com', 2),
                ('Ana', 'López', '3003456789', 'ana.lopez@clinica.com', 3),
                ('Luis', 'Martínez', '3004567890', 'luis.martinez@clinica.com', 4),
                ('Patricia', 'Hernández', '3005678901', 'patricia.hernandez@clinica.com', 5)
            ]
            
            for doctor in doctores:
                cursor.execute("INSERT INTO doctor (nombre, apellido, telefono, email, id_especialidad) VALUES (%s, %s, %s, %s, %s)", doctor)
            
            # Insertar pacientes de ejemplo
            pacientes = [
                ('Juan', 'Pérez', '1990-05-15', '3001111111', 'juan.perez@email.com', 'Calle 123 #45-67'),
                ('María', 'González', '1985-08-22', '3002222222', 'maria.gonzalez@email.com', 'Carrera 78 #90-12'),
                ('Pedro', 'Sánchez', '1995-03-10', '3003333333', 'pedro.sanchez@email.com', 'Avenida 5 #23-45'),
                ('Ana', 'Ramírez', '1988-12-05', '3004444444', 'ana.ramirez@email.com', 'Calle 67 #89-01'),
                ('Luis', 'Torres', '1992-07-18', '3005555555', 'luis.torres@email.com', 'Carrera 34 #56-78')
            ]
            
            for paciente in pacientes:
                cursor.execute("INSERT INTO paciente (nombre, apellido, fecha_nacimiento, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s, %s)", paciente)
            
            # Insertar citas de ejemplo
            citas = [
                ('2024-01-15 10:00:00', 'Consulta de rutina', 1, 1),
                ('2024-01-15 14:30:00', 'Revisión de piel', 2, 2),
                ('2024-01-16 09:00:00', 'Control pediátrico', 3, 3),
                ('2024-01-16 11:30:00', 'Consulta ginecológica', 4, 4),
                ('2024-01-17 15:00:00', 'Revisión ortopédica', 5, 5)
            ]
            
            for cita in citas:
                cursor.execute("INSERT INTO cita (fecha_hora, motivo, id_paciente, id_doctor) VALUES (%s, %s, %s, %s)", cita)
            
            # Insertar historiales de ejemplo
            historiales = [
                ('2024-01-10', 'Hipertensión arterial', 'Enalapril 10mg diario', 'Paciente con presión arterial elevada', 1, 1),
                ('2024-01-12', 'Dermatitis atópica', 'Cremas hidratantes y antihistamínicos', 'Paciente con piel seca y picazón', 2, 2),
                ('2024-01-08', 'Resfriado común', 'Reposo y líquidos abundantes', 'Paciente con síntomas leves', 3, 3),
                ('2024-01-05', 'Control ginecológico normal', 'Sin tratamiento requerido', 'Paciente en buen estado de salud', 4, 4),
                ('2024-01-03', 'Esguince de tobillo', 'Reposo, hielo y elevación', 'Paciente con lesión deportiva', 5, 5)
            ]
            
            for historial in historiales:
                cursor.execute("INSERT INTO historial (fecha, diagnostico, tratamiento, observaciones, id_paciente, id_doctor) VALUES (%s, %s, %s, %s, %s, %s)", historial)
            
            connection.commit()
            print("✅ Datos de ejemplo insertados")
        else:
            print("ℹ️  Los datos de ejemplo ya existen")
        
        # Crear índices para optimizar consultas
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_cita_fecha_hora ON cita(fecha_hora)",
            "CREATE INDEX IF NOT EXISTS idx_cita_paciente ON cita(id_paciente)",
            "CREATE INDEX IF NOT EXISTS idx_cita_doctor ON cita(id_doctor)",
            "CREATE INDEX IF NOT EXISTS idx_historial_paciente ON historial(id_paciente)",
            "CREATE INDEX IF NOT EXISTS idx_historial_fecha ON historial(fecha)",
            "CREATE INDEX IF NOT EXISTS idx_doctor_especialidad ON doctor(id_especialidad)"
        ]
        
        for index_sql in indices:
            try:
                cursor.execute(index_sql)
                connection.commit()
            except Error as e:
                if "already exists" not in str(e).lower():
                    print(f"⚠️  Advertencia creando índice: {e}")
        
        print("✅ Índices creados/verificados")
        print("🎉 Base de datos inicializada correctamente")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False
