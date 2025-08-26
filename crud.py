from database import execute_query, execute_query_one
from models import *
from typing import List, Optional
from datetime import date, datetime, timedelta

# ===========================================
# CRUD para Paciente
# ===========================================
def crear_paciente(paciente: PacienteCreate) -> Optional[int]:
    query = """
    INSERT INTO paciente (nombre, apellido, fecha_nacimiento, telefono, email, direccion)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        paciente.nombre, paciente.apellido, paciente.fecha_nacimiento,
        paciente.telefono, paciente.email, paciente.direccion
    )
    return execute_query(query, params)

def obtener_paciente(id_paciente: int) -> Optional[dict]:
    query = "SELECT * FROM paciente WHERE id_paciente = %s"
    return execute_query_one(query, (id_paciente,))

def obtener_pacientes() -> List[dict]:
    query = "SELECT * FROM paciente ORDER BY apellido, nombre"
    return execute_query(query, fetch=True) or []

def actualizar_paciente(id_paciente: int, paciente: PacienteUpdate) -> bool:
    # Construir query dinámicamente basado en campos no nulos
    fields = []
    params = []
    
    if paciente.nombre is not None:
        fields.append("nombre = %s")
        params.append(paciente.nombre)
    if paciente.apellido is not None:
        fields.append("apellido = %s")
        params.append(paciente.apellido)
    if paciente.fecha_nacimiento is not None:
        fields.append("fecha_nacimiento = %s")
        params.append(paciente.fecha_nacimiento)
    if paciente.telefono is not None:
        fields.append("telefono = %s")
        params.append(paciente.telefono)
    if paciente.email is not None:
        fields.append("email = %s")
        params.append(paciente.email)
    if paciente.direccion is not None:
        fields.append("direccion = %s")
        params.append(paciente.direccion)
    
    if not fields:
        return False
    
    params.append(id_paciente)
    query = f"UPDATE paciente SET {', '.join(fields)} WHERE id_paciente = %s"
    return execute_query(query, tuple(params)) is not None

def eliminar_paciente(id_paciente: int) -> bool:
    query = "DELETE FROM paciente WHERE id_paciente = %s"
    return execute_query(query, (id_paciente,)) is not None

# ===========================================
# CRUD para Especialidad
# ===========================================
def crear_especialidad(especialidad: EspecialidadCreate) -> Optional[int]:
    query = "INSERT INTO especialidad (nombre, descripcion) VALUES (%s, %s)"
    params = (especialidad.nombre, especialidad.descripcion)
    return execute_query(query, params)

def obtener_especialidad(id_especialidad: int) -> Optional[dict]:
    query = "SELECT * FROM especialidad WHERE id_especialidad = %s"
    return execute_query_one(query, (id_especialidad,))

def obtener_especialidades() -> List[dict]:
    query = "SELECT * FROM especialidad ORDER BY nombre"
    return execute_query(query, fetch=True) or []

def actualizar_especialidad(id_especialidad: int, especialidad: EspecialidadUpdate) -> bool:
    fields = []
    params = []
    
    if especialidad.nombre is not None:
        fields.append("nombre = %s")
        params.append(especialidad.nombre)
    if especialidad.descripcion is not None:
        fields.append("descripcion = %s")
        params.append(especialidad.descripcion)
    
    if not fields:
        return False
    
    params.append(id_especialidad)
    query = f"UPDATE especialidad SET {', '.join(fields)} WHERE id_especialidad = %s"
    return execute_query(query, tuple(params)) is not None

def eliminar_especialidad(id_especialidad: int) -> bool:
    query = "DELETE FROM especialidad WHERE id_especialidad = %s"
    return execute_query(query, (id_especialidad,)) is not None

# ===========================================
# CRUD para Doctor
# ===========================================
def crear_doctor(doctor: DoctorCreate) -> Optional[int]:
    query = """
    INSERT INTO doctor (nombre, apellido, telefono, email, id_especialidad)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (doctor.nombre, doctor.apellido, doctor.telefono, doctor.email, doctor.id_especialidad)
    return execute_query(query, params)

def obtener_doctor(id_doctor: int) -> Optional[dict]:
    query = """
    SELECT d.*, e.nombre as especialidad_nombre 
    FROM doctor d 
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad 
    WHERE d.id_doctor = %s
    """
    return execute_query_one(query, (id_doctor,))

def obtener_doctores() -> List[dict]:
    query = """
    SELECT d.*, e.nombre as especialidad_nombre 
    FROM doctor d 
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad 
    ORDER BY d.apellido, d.nombre
    """
    return execute_query(query, fetch=True) or []

def obtener_doctores_por_especialidad(id_especialidad: int) -> List[dict]:
    query = """
    SELECT d.*, e.nombre as especialidad_nombre 
    FROM doctor d 
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad 
    WHERE d.id_especialidad = %s
    ORDER BY d.apellido, d.nombre
    """
    return execute_query(query, (id_especialidad,), fetch=True) or []

def actualizar_doctor(id_doctor: int, doctor: DoctorUpdate) -> bool:
    fields = []
    params = []
    
    if doctor.nombre is not None:
        fields.append("nombre = %s")
        params.append(doctor.nombre)
    if doctor.apellido is not None:
        fields.append("apellido = %s")
        params.append(doctor.apellido)
    if doctor.telefono is not None:
        fields.append("telefono = %s")
        params.append(doctor.telefono)
    if doctor.email is not None:
        fields.append("email = %s")
        params.append(doctor.email)
    if doctor.id_especialidad is not None:
        fields.append("id_especialidad = %s")
        params.append(doctor.id_especialidad)
    
    if not fields:
        return False
    
    params.append(id_doctor)
    query = f"UPDATE doctor SET {', '.join(fields)} WHERE id_doctor = %s"
    return execute_query(query, tuple(params)) is not None

def eliminar_doctor(id_doctor: int) -> bool:
    query = "DELETE FROM doctor WHERE id_doctor = %s"
    return execute_query(query, (id_doctor,)) is not None

# ===========================================
# CRUD para Historial
# ===========================================
def crear_historial(historial: HistorialCreate) -> Optional[int]:
    query = """
    INSERT INTO historial (fecha, diagnostico, tratamiento, observaciones, id_paciente, id_doctor)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        historial.fecha, historial.diagnostico, historial.tratamiento,
        historial.observaciones, historial.id_paciente, historial.id_doctor
    )
    return execute_query(query, params)

def obtener_historial(id_historial: int) -> Optional[dict]:
    query = """
    SELECT h.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido
    FROM historial h
    JOIN paciente p ON h.id_paciente = p.id_paciente
    JOIN doctor d ON h.id_doctor = d.id_doctor
    WHERE h.id_historial = %s
    """
    return execute_query_one(query, (id_historial,))

def obtener_historial_paciente(id_paciente: int) -> List[dict]:
    query = """
    SELECT h.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido
    FROM historial h
    JOIN paciente p ON h.id_paciente = p.id_paciente
    JOIN doctor d ON h.id_doctor = d.id_doctor
    WHERE h.id_paciente = %s
    ORDER BY h.fecha DESC
    """
    return execute_query(query, (id_paciente,), fetch=True) or []

def actualizar_historial(id_historial: int, historial: HistorialUpdate) -> bool:
    fields = []
    params = []
    
    if historial.fecha is not None:
        fields.append("fecha = %s")
        params.append(historial.fecha)
    if historial.diagnostico is not None:
        fields.append("diagnostico = %s")
        params.append(historial.diagnostico)
    if historial.tratamiento is not None:
        fields.append("tratamiento = %s")
        params.append(historial.tratamiento)
    if historial.observaciones is not None:
        fields.append("observaciones = %s")
        params.append(historial.observaciones)
    if historial.id_doctor is not None:
        fields.append("id_doctor = %s")
        params.append(historial.id_doctor)
    
    if not fields:
        return False
    
    params.append(id_historial)
    query = f"UPDATE historial SET {', '.join(fields)} WHERE id_historial = %s"
    return execute_query(query, tuple(params)) is not None

def eliminar_historial(id_historial: int) -> bool:
    query = "DELETE FROM historial WHERE id_historial = %s"
    return execute_query(query, (id_historial,)) is not None

# ===========================================
# CRUD para Cita
# ===========================================
def crear_cita(cita: CitaCreate) -> Optional[int]:
    query = """
    INSERT INTO cita (fecha_hora, motivo, id_paciente, id_doctor)
    VALUES (%s, %s, %s, %s)
    """
    params = (cita.fecha_hora, cita.motivo, cita.id_paciente, cita.id_doctor)
    return execute_query(query, params)

def obtener_cita(id_cita: int) -> Optional[dict]:
    query = """
    SELECT c.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido,
           e.nombre as especialidad_nombre
    FROM cita c
    JOIN paciente p ON c.id_paciente = p.id_paciente
    JOIN doctor d ON c.id_doctor = d.id_doctor
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad
    WHERE c.id_cita = %s
    """
    return execute_query_one(query, (id_cita,))

def obtener_citas() -> List[dict]:
    query = """
    SELECT c.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido,
           e.nombre as especialidad_nombre
    FROM cita c
    JOIN paciente p ON c.id_paciente = p.id_paciente
    JOIN doctor d ON c.id_doctor = d.id_doctor
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad
    ORDER BY c.fecha_hora
    """
    return execute_query(query, fetch=True) or []

def obtener_citas_paciente(id_paciente: int) -> List[dict]:
    query = """
    SELECT c.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido,
           e.nombre as especialidad_nombre
    FROM cita c
    JOIN paciente p ON c.id_paciente = p.id_paciente
    JOIN doctor d ON c.id_doctor = d.id_doctor
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad
    WHERE c.id_paciente = %s
    ORDER BY c.fecha_hora
    """
    return execute_query(query, (id_paciente,), fetch=True) or []

def obtener_citas_doctor(id_doctor: int) -> List[dict]:
    query = """
    SELECT c.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
           d.nombre as doctor_nombre, d.apellido as doctor_apellido,
           e.nombre as especialidad_nombre
    FROM cita c
    JOIN paciente p ON c.id_paciente = p.id_paciente
    JOIN doctor d ON c.id_doctor = d.id_doctor
    JOIN especialidad e ON d.id_especialidad = e.id_especialidad
    WHERE c.id_doctor = %s
    ORDER BY c.fecha_hora
    """
    return execute_query(query, (id_doctor,), fetch=True) or []

def actualizar_cita(id_cita: int, cita: CitaUpdate) -> bool:
    fields = []
    params = []
    
    if cita.fecha_hora is not None:
        fields.append("fecha_hora = %s")
        params.append(cita.fecha_hora)
    if cita.motivo is not None:
        fields.append("motivo = %s")
        params.append(cita.motivo)
    if cita.id_doctor is not None:
        fields.append("id_doctor = %s")
        params.append(cita.id_doctor)
    
    if not fields:
        return False
    
    params.append(id_cita)
    query = f"UPDATE cita SET {', '.join(fields)} WHERE id_cita = %s"
    return execute_query(query, tuple(params)) is not None

def eliminar_cita(id_cita: int) -> bool:
    query = "DELETE FROM cita WHERE id_cita = %s"
    return execute_query(query, (id_cita,)) is not None

# ===========================================
# Funciones de disponibilidad
# ===========================================
def verificar_disponibilidad(fecha: date, id_doctor: int, hora: str) -> bool:
    """Verifica si un doctor está disponible en una fecha y hora específica"""
    fecha_hora = datetime.combine(fecha, datetime.strptime(hora, "%H:%M").time())
    query = """
    SELECT COUNT(*) as count FROM cita 
    WHERE id_doctor = %s AND DATE(fecha_hora) = %s AND TIME(fecha_hora) = %s
    """
    result = execute_query_one(query, (id_doctor, fecha, hora))
    return result and result['count'] == 0

def obtener_horarios_disponibles(fecha: date, id_doctor: Optional[int] = None, id_especialidad: Optional[int] = None) -> List[dict]:
    """Obtiene horarios disponibles para una fecha específica"""
    horarios_base = [
        "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
        "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30"
    ]
    
    if id_doctor:
        # Filtrar por doctor específico
        doctores = [obtener_doctor(id_doctor)] if obtener_doctor(id_doctor) else []
    elif id_especialidad:
        # Filtrar por especialidad
        doctores = obtener_doctores_por_especialidad(id_especialidad)
    else:
        # Todos los doctores
        doctores = obtener_doctores()
    
    disponibilidad = []
    
    for doctor in doctores:
        horarios_disponibles = []
        for hora in horarios_base:
            if verificar_disponibilidad(fecha, doctor['id_doctor'], hora):
                horarios_disponibles.append(hora)
        
        if horarios_disponibles:
            disponibilidad.append({
                'doctor_id': doctor['id_doctor'],
                'doctor_nombre': f"{doctor['nombre']} {doctor['apellido']}",
                'especialidad': doctor.get('especialidad_nombre', ''),
                'horarios_disponibles': horarios_disponibles
            })
    
    return disponibilidad
