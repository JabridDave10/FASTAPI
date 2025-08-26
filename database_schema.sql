-- ===========================================
-- Sistema de Citas Médicas - Esquema de Base de Datos
-- ===========================================

-- Creación de base de datos
CREATE DATABASE IF NOT EXISTS sistema_citas;
USE sistema_citas;

-- ===========================================
-- Tabla Paciente
-- ===========================================
CREATE TABLE paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    email VARCHAR(120) UNIQUE,
    direccion VARCHAR(200)
);

-- ===========================================
-- Tabla Especialidad
-- ===========================================
CREATE TABLE especialidad (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- ===========================================
-- Tabla Doctor
-- ===========================================
CREATE TABLE doctor (
    id_doctor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(150) UNIQUE,
    id_especialidad INT NOT NULL,
    FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad)
);

-- ===========================================
-- Tabla Historial
-- ===========================================
CREATE TABLE historial (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    id_paciente INT NOT NULL,
    id_doctor INT NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor)
);

-- ===========================================
-- Tabla Citas
-- ===========================================
CREATE TABLE cita (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    motivo VARCHAR(255),
    id_paciente INT,
    id_doctor INT,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor)
);

-- ===========================================
-- Datos de ejemplo para pruebas
-- ===========================================

-- Insertar especialidades de ejemplo
INSERT INTO especialidad (nombre, descripcion) VALUES
('Cardiología', 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades del corazón'),
('Dermatología', 'Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de la piel'),
('Pediatría', 'Especialidad médica que se encarga del cuidado de la salud de los niños'),
('Ginecología', 'Especialidad médica que se encarga de la salud del sistema reproductor femenino'),
('Ortopedia', 'Especialidad médica que se encarga del diagnóstico y tratamiento de lesiones y enfermedades del sistema musculoesquelético');

-- Insertar doctores de ejemplo
INSERT INTO doctor (nombre, apellido, telefono, email, id_especialidad) VALUES
('María', 'García', '3001234567', 'maria.garcia@clinica.com', 1),
('Carlos', 'Rodríguez', '3002345678', 'carlos.rodriguez@clinica.com', 2),
('Ana', 'López', '3003456789', 'ana.lopez@clinica.com', 3),
('Luis', 'Martínez', '3004567890', 'luis.martinez@clinica.com', 4),
('Patricia', 'Hernández', '3005678901', 'patricia.hernandez@clinica.com', 5);

-- Insertar pacientes de ejemplo
INSERT INTO paciente (nombre, apellido, fecha_nacimiento, telefono, email, direccion) VALUES
('Juan', 'Pérez', '1990-05-15', '3001111111', 'juan.perez@email.com', 'Calle 123 #45-67'),
('María', 'González', '1985-08-22', '3002222222', 'maria.gonzalez@email.com', 'Carrera 78 #90-12'),
('Pedro', 'Sánchez', '1995-03-10', '3003333333', 'pedro.sanchez@email.com', 'Avenida 5 #23-45'),
('Ana', 'Ramírez', '1988-12-05', '3004444444', 'ana.ramirez@email.com', 'Calle 67 #89-01'),
('Luis', 'Torres', '1992-07-18', '3005555555', 'luis.torres@email.com', 'Carrera 34 #56-78');

-- Insertar citas de ejemplo
INSERT INTO cita (fecha_hora, motivo, id_paciente, id_doctor) VALUES
('2024-01-15 10:00:00', 'Consulta de rutina', 1, 1),
('2024-01-15 14:30:00', 'Revisión de piel', 2, 2),
('2024-01-16 09:00:00', 'Control pediátrico', 3, 3),
('2024-01-16 11:30:00', 'Consulta ginecológica', 4, 4),
('2024-01-17 15:00:00', 'Revisión ortopédica', 5, 5);

-- Insertar historiales de ejemplo
INSERT INTO historial (fecha, diagnostico, tratamiento, observaciones, id_paciente, id_doctor) VALUES
('2024-01-10', 'Hipertensión arterial', 'Enalapril 10mg diario', 'Paciente con presión arterial elevada', 1, 1),
('2024-01-12', 'Dermatitis atópica', 'Cremas hidratantes y antihistamínicos', 'Paciente con piel seca y picazón', 2, 2),
('2024-01-08', 'Resfriado común', 'Reposo y líquidos abundantes', 'Paciente con síntomas leves', 3, 3),
('2024-01-05', 'Control ginecológico normal', 'Sin tratamiento requerido', 'Paciente en buen estado de salud', 4, 4),
('2024-01-03', 'Esguince de tobillo', 'Reposo, hielo y elevación', 'Paciente con lesión deportiva', 5, 5);

-- ===========================================
-- Índices para optimizar consultas
-- ===========================================
CREATE INDEX idx_cita_fecha_hora ON cita(fecha_hora);
CREATE INDEX idx_cita_paciente ON cita(id_paciente);
CREATE INDEX idx_cita_doctor ON cita(id_doctor);
CREATE INDEX idx_historial_paciente ON historial(id_paciente);
CREATE INDEX idx_historial_fecha ON historial(fecha);
CREATE INDEX idx_doctor_especialidad ON doctor(id_especialidad);

-- ===========================================
-- Verificar la creación de las tablas
-- ===========================================
SHOW TABLES;

-- Verificar los datos insertados
SELECT 'Especialidades:' as info;
SELECT * FROM especialidad;

SELECT 'Doctores:' as info;
SELECT d.*, e.nombre as especialidad_nombre 
FROM doctor d 
JOIN especialidad e ON d.id_especialidad = e.id_especialidad;

SELECT 'Pacientes:' as info;
SELECT * FROM paciente;

SELECT 'Citas:' as info;
SELECT c.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
       d.nombre as doctor_nombre, d.apellido as doctor_apellido
FROM cita c
JOIN paciente p ON c.id_paciente = p.id_paciente
JOIN doctor d ON c.id_doctor = d.id_doctor;

SELECT 'Historiales:' as info;
SELECT h.*, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
       d.nombre as doctor_nombre, d.apellido as doctor_apellido
FROM historial h
JOIN paciente p ON h.id_paciente = p.id_paciente
JOIN doctor d ON h.id_doctor = d.id_doctor;
