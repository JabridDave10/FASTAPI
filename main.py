from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date, datetime
import crud
from models import *

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Citas Médicas",
    description="API REST para gestión de citas médicas, pacientes, doctores y especialidades",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# Endpoints para Paciente
# ===========================================
@app.post("/pacientes/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_paciente_endpoint(paciente: PacienteCreate):
    """Crear un nuevo paciente"""
    paciente_id = crud.crear_paciente(paciente)
    if paciente_id:
        return {"message": "Paciente creado exitosamente", "id_paciente": paciente_id}
    raise HTTPException(status_code=400, detail="Error al crear el paciente")

@app.get("/pacientes/", response_model=List[dict])
async def obtener_pacientes_endpoint():
    """Obtener todos los pacientes"""
    return crud.obtener_pacientes()

@app.get("/pacientes/{paciente_id}", response_model=dict)
async def obtener_paciente_endpoint(paciente_id: int):
    """Obtener un paciente específico por ID"""
    paciente = crud.obtener_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@app.put("/pacientes/{paciente_id}", response_model=dict)
async def actualizar_paciente_endpoint(paciente_id: int, paciente: PacienteUpdate):
    """Actualizar un paciente existente"""
    if not crud.obtener_paciente(paciente_id):
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    if crud.actualizar_paciente(paciente_id, paciente):
        return {"message": "Paciente actualizado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al actualizar el paciente")

@app.delete("/pacientes/{paciente_id}", response_model=dict)
async def eliminar_paciente_endpoint(paciente_id: int):
    """Eliminar un paciente"""
    if not crud.obtener_paciente(paciente_id):
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    if crud.eliminar_paciente(paciente_id):
        return {"message": "Paciente eliminado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar el paciente")

# ===========================================
# Endpoints para Especialidad
# ===========================================
@app.post("/especialidades/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_especialidad_endpoint(especialidad: EspecialidadCreate):
    """Crear una nueva especialidad"""
    especialidad_id = crud.crear_especialidad(especialidad)
    if especialidad_id:
        return {"message": "Especialidad creada exitosamente", "id_especialidad": especialidad_id}
    raise HTTPException(status_code=400, detail="Error al crear la especialidad")

@app.get("/especialidades/", response_model=List[dict])
async def obtener_especialidades_endpoint():
    """Obtener todas las especialidades"""
    return crud.obtener_especialidades()

@app.get("/especialidades/{especialidad_id}", response_model=dict)
async def obtener_especialidad_endpoint(especialidad_id: int):
    """Obtener una especialidad específica por ID"""
    especialidad = crud.obtener_especialidad(especialidad_id)
    if not especialidad:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    return especialidad

@app.put("/especialidades/{especialidad_id}", response_model=dict)
async def actualizar_especialidad_endpoint(especialidad_id: int, especialidad: EspecialidadUpdate):
    """Actualizar una especialidad existente"""
    if not crud.obtener_especialidad(especialidad_id):
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    
    if crud.actualizar_especialidad(especialidad_id, especialidad):
        return {"message": "Especialidad actualizada exitosamente"}
    raise HTTPException(status_code=400, detail="Error al actualizar la especialidad")

@app.delete("/especialidades/{especialidad_id}", response_model=dict)
async def eliminar_especialidad_endpoint(especialidad_id: int):
    """Eliminar una especialidad"""
    if not crud.obtener_especialidad(especialidad_id):
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    
    if crud.eliminar_especialidad(especialidad_id):
        return {"message": "Especialidad eliminada exitosamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar la especialidad")

# ===========================================
# Endpoints para Doctor
# ===========================================
@app.post("/doctores/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_doctor_endpoint(doctor: DoctorCreate):
    """Crear un nuevo doctor"""
    doctor_id = crud.crear_doctor(doctor)
    if doctor_id:
        return {"message": "Doctor creado exitosamente", "id_doctor": doctor_id}
    raise HTTPException(status_code=400, detail="Error al crear el doctor")

@app.get("/doctores/", response_model=List[dict])
async def obtener_doctores_endpoint():
    """Obtener todos los doctores"""
    return crud.obtener_doctores()

@app.get("/doctores/{doctor_id}", response_model=dict)
async def obtener_doctor_endpoint(doctor_id: int):
    """Obtener un doctor específico por ID"""
    doctor = crud.obtener_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor

@app.get("/doctores/especialidad/{especialidad_id}", response_model=List[dict])
async def obtener_doctores_por_especialidad_endpoint(especialidad_id: int):
    """Obtener doctores por especialidad"""
    return crud.obtener_doctores_por_especialidad(especialidad_id)

@app.put("/doctores/{doctor_id}", response_model=dict)
async def actualizar_doctor_endpoint(doctor_id: int, doctor: DoctorUpdate):
    """Actualizar un doctor existente"""
    if not crud.obtener_doctor(doctor_id):
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    
    if crud.actualizar_doctor(doctor_id, doctor):
        return {"message": "Doctor actualizado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al actualizar el doctor")

@app.delete("/doctores/{doctor_id}", response_model=dict)
async def eliminar_doctor_endpoint(doctor_id: int):
    """Eliminar un doctor"""
    if not crud.obtener_doctor(doctor_id):
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    
    if crud.eliminar_doctor(doctor_id):
        return {"message": "Doctor eliminado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar el doctor")

# ===========================================
# Endpoints para Historial
# ===========================================
@app.post("/historial/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_historial_endpoint(historial: HistorialCreate):
    """Crear un nuevo registro de historial"""
    historial_id = crud.crear_historial(historial)
    if historial_id:
        return {"message": "Historial creado exitosamente", "id_historial": historial_id}
    raise HTTPException(status_code=400, detail="Error al crear el historial")

@app.get("/historial/{historial_id}", response_model=dict)
async def obtener_historial_endpoint(historial_id: int):
    """Obtener un registro de historial específico por ID"""
    historial = crud.obtener_historial(historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial

@app.get("/historial/paciente/{paciente_id}", response_model=List[dict])
async def obtener_historial_paciente_endpoint(paciente_id: int):
    """Obtener historial médico de un paciente"""
    return crud.obtener_historial_paciente(paciente_id)

@app.put("/historial/{historial_id}", response_model=dict)
async def actualizar_historial_endpoint(historial_id: int, historial: HistorialUpdate):
    """Actualizar un registro de historial existente"""
    if not crud.obtener_historial(historial_id):
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    if crud.actualizar_historial(historial_id, historial):
        return {"message": "Historial actualizado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al actualizar el historial")

@app.delete("/historial/{historial_id}", response_model=dict)
async def eliminar_historial_endpoint(historial_id: int):
    """Eliminar un registro de historial"""
    if not crud.obtener_historial(historial_id):
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    if crud.eliminar_historial(historial_id):
        return {"message": "Historial eliminado exitosamente"}
    raise HTTPException(status_code=400, detail="Error al eliminar el historial")

# ===========================================
# Endpoints para Cita
# ===========================================
@app.post("/citas/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def crear_cita_endpoint(cita: CitaCreate):
    """Crear una nueva cita"""
    cita_id = crud.crear_cita(cita)
    if cita_id:
        return {"message": "Cita creada exitosamente", "id_cita": cita_id}
    raise HTTPException(status_code=400, detail="Error al crear la cita")

@app.get("/citas/", response_model=List[dict])
async def obtener_citas_endpoint():
    """Obtener todas las citas"""
    return crud.obtener_citas()

@app.get("/citas/{cita_id}", response_model=dict)
async def obtener_cita_endpoint(cita_id: int):
    """Obtener una cita específica por ID"""
    cita = crud.obtener_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@app.get("/citas/paciente/{paciente_id}", response_model=List[dict])
async def obtener_citas_paciente_endpoint(paciente_id: int):
    """Obtener citas de un paciente específico"""
    return crud.obtener_citas_paciente(paciente_id)

@app.get("/citas/doctor/{doctor_id}", response_model=List[dict])
async def obtener_citas_doctor_endpoint(doctor_id: int):
    """Obtener citas de un doctor específico"""
    return crud.obtener_citas_doctor(doctor_id)

@app.put("/citas/{cita_id}", response_model=dict)
async def actualizar_cita_endpoint(cita_id: int, cita: CitaUpdate):
    """Actualizar una cita existente"""
    if not crud.obtener_cita(cita_id):
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    if crud.actualizar_cita(cita_id, cita):
        return {"message": "Cita actualizada exitosamente"}
    raise HTTPException(status_code=400, detail="Error al actualizar la cita")

@app.delete("/citas/{cita_id}", response_model=dict)
async def eliminar_cita_endpoint(cita_id: int):
    """Cancelar/eliminar una cita"""
    if not crud.obtener_cita(cita_id):
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    if crud.eliminar_cita(cita_id):
        return {"message": "Cita cancelada exitosamente"}
    raise HTTPException(status_code=400, detail="Error al cancelar la cita")

# ===========================================
# Endpoints para Disponibilidad
# ===========================================
@app.get("/disponibilidad/", response_model=List[dict])
async def obtener_disponibilidad_endpoint(
    fecha: date,
    id_doctor: Optional[int] = None,
    id_especialidad: Optional[int] = None
):
    """Obtener horarios disponibles para una fecha específica"""
    return crud.obtener_horarios_disponibles(fecha, id_doctor, id_especialidad)

@app.get("/disponibilidad/verificar/")
async def verificar_disponibilidad_endpoint(
    fecha: date,
    id_doctor: int,
    hora: str
):
    """Verificar si un doctor está disponible en una fecha y hora específica"""
    disponible = crud.verificar_disponibilidad(fecha, id_doctor, hora)
    return {
        "fecha": fecha,
        "id_doctor": id_doctor,
        "hora": hora,
        "disponible": disponible
    }

# ===========================================
# Endpoint de salud
# ===========================================
@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Sistema de Citas Médicas API",
        "version": "1.0.0",
        "endpoints": {
            "pacientes": "/pacientes/",
            "especialidades": "/especialidades/",
            "doctores": "/doctores/",
            "historial": "/historial/",
            "citas": "/citas/",
            "disponibilidad": "/disponibilidad/",
            "documentacion": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
