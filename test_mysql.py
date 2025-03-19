import mysql.connector
import time

print("Intentando conectar a MySQL...")
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        connect_timeout=5
    )
    print("¡Conexión exitosa a MySQL!")
    connection.close()
except Exception as e:
    print(f"Error al conectar: {e}")

print("Esperando 5 segundos antes de cerrar...")
time.sleep(5)