import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

class Config:
    # Configuración general
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'coquito_amarillo_secret_key'
    
    # Configuración de la base de datos
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'coquito'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3307)
    
    # Configuración de directorios de datos
    DATA_DIR = os.environ.get('DATA_DIR') or 'data'
    CSV_DIR = os.path.join(DATA_DIR, 'csv')
    JSON_DIR = os.path.join(DATA_DIR, 'json')
    
    # Asegurar que existen los directorios
    @staticmethod
    def init_app(app):
        os.makedirs(Config.CSV_DIR, exist_ok=True)
        os.makedirs(Config.JSON_DIR, exist_ok=True)