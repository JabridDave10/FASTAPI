import mysql.connector
from mysql.connector import Error
from typing import Optional

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # Cambiar según tu configuración
    "database": "sistema_citas"
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
