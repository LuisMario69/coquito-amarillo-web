# app/__init__.py modificado
import mysql.connector
from mysql.connector import Error
import time

def init_db():
    # Primero conecta sin especificar base de datos
    print("Intentando conectar a MySQL...")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            connect_timeout=5  # Añadir timeout de 5 segundos
        )
        print("Conexión exitosa a MySQL")
        
        cursor = connection.cursor()
        
        # Crear base de datos si no existe
        print("Creando base de datos si no existe...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS lifemetrics")
        print("Base de datos 'lifemetrics' verificada/creada")
        
        # Seleccionar base de datos
        cursor.execute("USE lifemetrics")
        
        # Crear tabla si no existe
        print("Creando tabla si no existe...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rueda_vida (
            id INT AUTO_INCREMENT PRIMARY KEY,
            categoria VARCHAR(100) NOT NULL,
            valor INT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY (categoria)
        )
        """)
        print("Tabla 'rueda_vida' verificada/creada")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"Error inicializando BD: {e}")
        return False