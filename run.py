# run.py con mensajes de diagnóstico
import logging
import sys
import time

# Configuración del logger para mostrar todo en consola
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("=== INICIANDO APLICACIÓN ===")
logger.info("Python path: " + str(sys.path))

try:
    logger.info("Intentando importar init_db...")
    from app import init_db
    logger.info("Importación de init_db exitosa")
    
    logger.info("Intentando importar create_app...")
    from app.main import create_app
    logger.info("Importación de create_app exitosa")
    
    if __name__ == "__main__":
        try:
            # Inicializar base de datos
            logger.info("Inicializando base de datos...")
            result = init_db()
            logger.info(f"Base de datos inicializada: {result}")
            
            # Crear y ejecutar la aplicación
            logger.info("Creando aplicación Flask...")
            app = create_app()
            logger.info("Aplicación creada, iniciando servidor...")
            app.run(debug=True, use_reloader=False)
        except Exception as e:
            logger.error(f"Error crítico: {e}", exc_info=True)
            time.sleep(5)  # Pausa para que puedas ver el error antes de que se cierre la consola
except ImportError as e:
    logger.error(f"Error importando módulos: {e}", exc_info=True)
    time.sleep(5)  # Pausa para que puedas ver el error
except Exception as e:
    logger.error(f"Error desconocido: {e}", exc_info=True)
    time.sleep(5)  # Pausa para que puedas ver el error