#!/usr/bin/env python3
"""
Script de configuración para el Sistema de Citas Médicas
Este script ayuda a configurar la base de datos y verificar la conexión
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def test_database_connection(config):
    """Prueba la conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Conexión exitosa a MySQL Server versión {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"✅ Conectado a la base de datos: {record[0]}")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return False

def create_database_if_not_exists(config):
    """Crea la base de datos si no existe"""
    try:
        # Conectar sin especificar base de datos
        config_without_db = config.copy()
        del config_without_db['database']
        
        connection = mysql.connector.connect(**config_without_db)
        cursor = connection.cursor()
        
        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        print(f"✅ Base de datos '{config['database']}' creada/verificada")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def execute_sql_file(config, sql_file):
    """Ejecuta un archivo SQL"""
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
        
        # Dividir por comandos SQL (separados por ;)
        commands = sql_commands.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    connection.commit()
                except Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️  Advertencia ejecutando comando: {e}")
        
        print(f"✅ Archivo SQL '{sql_file}' ejecutado correctamente")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error ejecutando archivo SQL: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Archivo SQL '{sql_file}' no encontrado")
        return False

def get_database_config():
    """Obtiene la configuración de la base de datos del usuario"""
    print("🔧 Configuración de la Base de Datos")
    print("=" * 40)
    
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Puerto (default: 3306): ").strip() or "3306"
    user = input("Usuario MySQL: ").strip()
    password = input("Contraseña MySQL: ").strip()
    database = input("Nombre de la base de datos (default: sistema_citas): ").strip() or "sistema_citas"
    
    return {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "database": database
    }

def update_database_file(config):
    """Actualiza el archivo database.py con la nueva configuración"""
    try:
        with open('database.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Reemplazar la configuración
        new_config = f'''# Configuración de la base de datos
DB_CONFIG = {{
    "host": "{config['host']}",
    "port": {config['port']},
    "user": "{config['user']}",
    "password": "{config['password']}",
    "database": "{config['database']}"
}}'''
        
        # Buscar y reemplazar la configuración existente
        import re
        pattern = r'DB_CONFIG = \{[\s\S]*?\}'
        new_content = re.sub(pattern, new_config, content)
        
        with open('database.py', 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print("✅ Archivo database.py actualizado")
        return True
    except Exception as e:
        print(f"❌ Error actualizando database.py: {e}")
        return False

def main():
    """Función principal del script de configuración"""
    print("🚀 CONFIGURACIÓN DEL SISTEMA DE CITAS MÉDICAS")
    print("=" * 50)
    
    # Obtener configuración
    config = get_database_config()
    
    print(f"\n📋 Configuración a usar:")
    print(f"   Host: {config['host']}")
    print(f"   Puerto: {config['port']}")
    print(f"   Usuario: {config['user']}")
    print(f"   Base de datos: {config['database']}")
    
    # Probar conexión inicial
    print(f"\n🔍 Probando conexión inicial...")
    if not test_database_connection(config):
        print("❌ No se pudo conectar a MySQL. Verifica:")
        print("   - Que MySQL esté ejecutándose")
        print("   - Que las credenciales sean correctas")
        print("   - Que el usuario tenga permisos")
        return False
    
    # Crear base de datos si no existe
    print(f"\n🗄️  Verificando base de datos...")
    if not create_database_if_not_exists(config):
        return False
    
    # Ejecutar script SQL
    print(f"\n📝 Ejecutando script de base de datos...")
    if not execute_sql_file(config, 'database_schema.sql'):
        return False
    
    # Actualizar archivo database.py
    print(f"\n⚙️  Actualizando configuración...")
    if not update_database_file(config):
        return False
    
    # Prueba final
    print(f"\n✅ Prueba final de conexión...")
    if test_database_connection(config):
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Instalar dependencias: pip install -r requirements.txt")
        print("   2. Ejecutar la API: python main.py")
        print("   3. Probar la API: python test_api.py")
        print("   4. Ver documentación: http://localhost:8000/docs")
        return True
    else:
        print("❌ Error en la prueba final")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
