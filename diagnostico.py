# diagnostico.py
import sys
import time
import logging
import mysql.connector

# Configuramos logging para ver todos los mensajes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=== INICIANDO DIAGNÓSTICO ===")
    
    # Paso 1: Verificar versión de Python
    logger.info(f"Versión de Python: {sys.version}")
    
    # Paso 2: Intentar importar módulos clave
    try:
        logger.info("Importando módulos...")
        import flask
        logger.info(f"Flask versión: {flask.__version__}")
        import pandas as pd
        logger.info(f"Pandas versión: {pd.__version__}")
        import plotly
        logger.info(f"Plotly versión: {plotly.__version__}")
    except ImportError as e:
        logger.error(f"Error importando módulos: {e}")
        return
    
    # Paso 3: Verificar conexión a MySQL
    logger.info("Probando conexión a MySQL...")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            connect_timeout=5
        )
        if connection.is_connected():
            logger.info("Conexión a MySQL exitosa")
            connection.close()
        else:
            logger.error("No se pudo conectar a MySQL")
            return
    except Exception as e:
        logger.error(f"Error conectando a MySQL: {e}")
        return
    
    # Paso 4: Verificar existencia de base de datos
    logger.info("Verificando base de datos 'lifemetrics'...")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            connect_timeout=5
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'lifemetrics'")
        result = cursor.fetchone()
        if result:
            logger.info("Base de datos 'lifemetrics' existe")
            
            # Verificar tabla
            cursor.execute("USE lifemetrics")
            cursor.execute("SHOW TABLES LIKE 'rueda_vida'")
            result = cursor.fetchone()
            if result:
                logger.info("Tabla 'rueda_vida' existe")
                
                # Contar registros
                cursor.execute("SELECT COUNT(*) FROM rueda_vida")
                count = cursor.fetchone()[0]
                logger.info(f"Número de registros en 'rueda_vida': {count}")
            else:
                logger.warning("Tabla 'rueda_vida' no existe")
        else:
            logger.warning("Base de datos 'lifemetrics' no existe")
        
        cursor.close()
        connection.close()
    except Exception as e:
        logger.error(f"Error verificando base de datos: {e}")
        return
    
    # Paso 5: Intentar importar nuestros propios módulos
    logger.info("Intentando importar módulos del proyecto...")
    try:
        sys.path.append('.')  # Asegura que podemos importar desde el directorio actual
        from app import init_db
        logger.info("Módulo 'app.init_db' importado correctamente")
        from app.main import create_app
        logger.info("Módulo 'app.main.create_app' importado correctamente")
    except Exception as e:
        logger.error(f"Error importando módulos del proyecto: {e}")
        return
    
    logger.info("=== DIAGNÓSTICO COMPLETADO ===")
    logger.info("Todos los componentes parecen estar funcionando correctamente")
    logger.info("Intenta ejecutar 'python run.py' nuevamente")

if __name__ == "__main__":
    main()