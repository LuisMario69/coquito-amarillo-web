import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lifemetrics",
            connect_timeout=10  # Añadir timeout para evitar bloqueos
        )
        if connection.is_connected():
            return connection
        else:
            logger.error("Conexión creada pero no conectada")
            return None
    except Error as e:
        import traceback
        logger.error(f"Error connecting to MySQL: {e}")
        logger.error(traceback.format_exc())
        return None

def close_db_connection(connection):
    if connection and connection.is_connected():
        connection.close()