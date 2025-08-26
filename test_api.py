#!/usr/bin/env python3
"""
Script de prueba para el Sistema de Citas Médicas API
Este script demuestra cómo usar los diferentes endpoints de la API
"""

import requests
import json
from datetime import date, datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def print_response(response, title):
    """Imprime la respuesta de la API de forma legible"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*50}")

def test_pacientes():
    """Prueba los endpoints de pacientes"""
    print("\n🧪 Probando endpoints de PACIENTES...")
    
    # Crear un nuevo paciente
    nuevo_paciente = {
        "nombre": "Roberto",
        "apellido": "Silva",
        "fecha_nacimiento": "1987-11-20",
        "telefono": "3006666666",
        "email": "roberto.silva@email.com",
        "direccion": "Calle 45 #67-89"
    }
    
    response = requests.post(f"{BASE_URL}/pacientes/", 
                           json=nuevo_paciente, headers=HEADERS)
    print_response(response, "CREAR PACIENTE")
    
    if response.status_code == 201:
        paciente_id = response.json().get("id_paciente")
        
        # Obtener todos los pacientes
        response = requests.get(f"{BASE_URL}/pacientes/")
        print_response(response, "OBTENER TODOS LOS PACIENTES")
        
        # Obtener paciente específico
        response = requests.get(f"{BASE_URL}/pacientes/{paciente_id}")
        print_response(response, f"OBTENER PACIENTE {paciente_id}")
        
        # Actualizar paciente
        actualizacion = {
            "telefono": "3007777777",
            "direccion": "Calle 45 #67-89, Apto 101"
        }
        response = requests.put(f"{BASE_URL}/pacientes/{paciente_id}", 
                              json=actualizacion, headers=HEADERS)
        print_response(response, f"ACTUALIZAR PACIENTE {paciente_id}")

def test_especialidades():
    """Prueba los endpoints de especialidades"""
    print("\n🧪 Probando endpoints de ESPECIALIDADES...")
    
    # Crear una nueva especialidad
    nueva_especialidad = {
        "nombre": "Neurología",
        "descripcion": "Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del sistema nervioso"
    }
    
    response = requests.post(f"{BASE_URL}/especialidades/", 
                           json=nueva_especialidad, headers=HEADERS)
    print_response(response, "CREAR ESPECIALIDAD")
    
    if response.status_code == 201:
        especialidad_id = response.json().get("id_especialidad")
        
        # Obtener todas las especialidades
        response = requests.get(f"{BASE_URL}/especialidades/")
        print_response(response, "OBTENER TODAS LAS ESPECIALIDADES")
        
        # Obtener especialidad específica
        response = requests.get(f"{BASE_URL}/especialidades/{especialidad_id}")
        print_response(response, f"OBTENER ESPECIALIDAD {especialidad_id}")

def test_doctores():
    """Prueba los endpoints de doctores"""
    print("\n🧪 Probando endpoints de DOCTORES...")
    
    # Crear un nuevo doctor
    nuevo_doctor = {
        "nombre": "Fernando",
        "apellido": "Vargas",
        "telefono": "3008888888",
        "email": "fernando.vargas@clinica.com",
        "id_especialidad": 1  # Cardiología
    }
    
    response = requests.post(f"{BASE_URL}/doctores/", 
                           json=nuevo_doctor, headers=HEADERS)
    print_response(response, "CREAR DOCTOR")
    
    if response.status_code == 201:
        doctor_id = response.json().get("id_doctor")
        
        # Obtener todos los doctores
        response = requests.get(f"{BASE_URL}/doctores/")
        print_response(response, "OBTENER TODOS LOS DOCTORES")
        
        # Obtener doctores por especialidad
        response = requests.get(f"{BASE_URL}/doctores/especialidad/1")
        print_response(response, "OBTENER DOCTORES POR ESPECIALIDAD (Cardiología)")

def test_citas():
    """Prueba los endpoints de citas"""
    print("\n🧪 Probando endpoints de CITAS...")
    
    # Crear una nueva cita
    nueva_cita = {
        "fecha_hora": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT10:00:00"),
        "motivo": "Consulta de seguimiento",
        "id_paciente": 1,
        "id_doctor": 1
    }
    
    response = requests.post(f"{BASE_URL}/citas/", 
                           json=nueva_cita, headers=HEADERS)
    print_response(response, "CREAR CITA")
    
    if response.status_code == 201:
        cita_id = response.json().get("id_cita")
        
        # Obtener todas las citas
        response = requests.get(f"{BASE_URL}/citas/")
        print_response(response, "OBTENER TODAS LAS CITAS")
        
        # Obtener citas de un paciente
        response = requests.get(f"{BASE_URL}/citas/paciente/1")
        print_response(response, "OBTENER CITAS DEL PACIENTE 1")
        
        # Obtener citas de un doctor
        response = requests.get(f"{BASE_URL}/citas/doctor/1")
        print_response(response, "OBTENER CITAS DEL DOCTOR 1")

def test_historial():
    """Prueba los endpoints de historial"""
    print("\n🧪 Probando endpoints de HISTORIAL...")
    
    # Crear un nuevo registro de historial
    nuevo_historial = {
        "fecha": date.today().strftime("%Y-%m-%d"),
        "diagnostico": "Control rutinario",
        "tratamiento": "Sin tratamiento requerido",
        "observaciones": "Paciente en buen estado de salud general",
        "id_paciente": 1,
        "id_doctor": 1
    }
    
    response = requests.post(f"{BASE_URL}/historial/", 
                           json=nuevo_historial, headers=HEADERS)
    print_response(response, "CREAR HISTORIAL")
    
    if response.status_code == 201:
        historial_id = response.json().get("id_historial")
        
        # Obtener historial de un paciente
        response = requests.get(f"{BASE_URL}/historial/paciente/1")
        print_response(response, "OBTENER HISTORIAL DEL PACIENTE 1")

def test_disponibilidad():
    """Prueba los endpoints de disponibilidad"""
    print("\n🧪 Probando endpoints de DISPONIBILIDAD...")
    
    # Obtener disponibilidad para una fecha específica
    fecha_consulta = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = requests.get(f"{BASE_URL}/disponibilidad/?fecha={fecha_consulta}")
    print_response(response, f"OBTENER DISPONIBILIDAD PARA {fecha_consulta}")
    
    # Verificar disponibilidad específica
    response = requests.get(f"{BASE_URL}/disponibilidad/verificar/?fecha={fecha_consulta}&id_doctor=1&hora=09:00")
    print_response(response, "VERIFICAR DISPONIBILIDAD ESPECÍFICA")

def test_root():
    """Prueba el endpoint raíz"""
    print("\n🧪 Probando endpoint raíz...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "ENDPOINT RAÍZ")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE CITAS MÉDICAS")
    print("=" * 60)
    
    try:
        # Probar endpoint raíz
        test_root()
        
        # Probar cada módulo
        test_pacientes()
        test_especialidades()
        test_doctores()
        test_citas()
        test_historial()
        test_disponibilidad()
        
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("\n📖 Para ver la documentación interactiva, visita:")
        print(f"   {BASE_URL}/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
