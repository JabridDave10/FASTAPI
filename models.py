from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# ===========================================
# Modelos para Paciente
# ===========================================
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None

class Paciente(PacienteBase):
    id_paciente: int
    
    class Config:
        from_attributes = True

# ===========================================
# Modelos para Especialidad
# ===========================================
class EspecialidadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class Especialidad(EspecialidadBase):
    id_especialidad: int
    
    class Config:
        from_attributes = True

# ===========================================
# Modelos para Doctor
# ===========================================
class DoctorBase(BaseModel):
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    id_especialidad: int

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    id_especialidad: Optional[int] = None

class Doctor(DoctorBase):
    id_doctor: int
    
    class Config:
        from_attributes = True

# ===========================================
# Modelos para Historial
# ===========================================
class HistorialBase(BaseModel):
    fecha: date
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    id_paciente: int
    id_doctor: int

class HistorialCreate(HistorialBase):
    pass

class HistorialUpdate(BaseModel):
    fecha: Optional[date] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    id_doctor: Optional[int] = None

class Historial(HistorialBase):
    id_historial: int
    
    class Config:
        from_attributes = True

# ===========================================
# Modelos para Cita
# ===========================================
class CitaBase(BaseModel):
    fecha_hora: datetime
    motivo: Optional[str] = None
    id_paciente: int
    id_doctor: int

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    id_doctor: Optional[int] = None

class Cita(CitaBase):
    id_cita: int
    
    class Config:
        from_attributes = True

# ===========================================
# Modelos para respuestas de disponibilidad
# ===========================================
class DisponibilidadRequest(BaseModel):
    fecha: date
    id_doctor: Optional[int] = None
    id_especialidad: Optional[int] = None

class DisponibilidadResponse(BaseModel):
    fecha: date
    doctor: str
    especialidad: str
    horarios_disponibles: list[str]
