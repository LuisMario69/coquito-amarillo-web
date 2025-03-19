from app.database import get_db_connection
import logging

logger = logging.getLogger(__name__)

class RuedaVida:
    @staticmethod
    def get_preguntas():
        return [
            "Carrera: ¿Estás satisfecho con tu progreso profesional?",
            "Finanzas: ¿Sientes que tienes control sobre tu situación económica?",
            "Salud: ¿Cuidas regularmente de tu bienestar físico y mental?",
            "Relaciones Personales: ¿Mantienes conexiones significativas con familia y amigos?",
            "Crecimiento Personal: ¿Inviertes tiempo en tu desarrollo personal?",
            "Espiritualidad: ¿Sientes que tu vida tiene un propósito más profundo?",
            "Diversión/Ocio: ¿Disfrutas y te diviertes regularmente?",
            "Entorno/Ambiente: ¿Te sientes cómodo y satisfecho con tu entorno?"
        ]
    
    @staticmethod
    def guardar_respuesta(categoria, valor):
        try:
            conn = get_db_connection()
            if not conn:
                logger.error("No se pudo conectar a la base de datos")
                return False
                
            cursor = conn.cursor()
            
            # Usar ON DUPLICATE KEY UPDATE para actualizar si ya existe
            query = """
            INSERT INTO rueda_vida (categoria, valor) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE valor = %s
            """
            cursor.execute(query, (categoria, valor, valor))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error al guardar respuesta: {e}")
            return False
    
    @staticmethod
    def get_all_data():
        try:
            conn = get_db_connection()
            if not conn:
                return []
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT categoria, valor FROM rueda_vida")
            
            result = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error al obtener datos: {e}")
            return []