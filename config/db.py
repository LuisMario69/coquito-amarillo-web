import mysql.connector
from config.config import Config

class Database:
    @staticmethod
    def get_connection():
        """Establece conexión con la base de datos MySQL"""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                port=Config.MYSQL_PORT,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error al conectar a MySQL: {err}")
            return None
    
    @staticmethod
    def init_db():
        """Inicializa la base de datos creando las tablas necesarias"""
        conn = Database.get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Encuesta (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    empleado_id VARCHAR(50) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    departamento VARCHAR(50) NOT NULL,
                    fecha_evaluacion DATE NOT NULL,
                    salud INT NOT NULL,
                    carrera INT NOT NULL,
                    finanzas INT NOT NULL,
                    relaciones INT NOT NULL,
                    crecimiento INT NOT NULL,
                    ocio INT NOT NULL,
                    entorno INT NOT NULL,
                    proposito INT NOT NULL,
                    objetivos TEXT,
                    apoyo TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crear índices útiles
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_empleado_id ON Encuesta(empleado_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_departamento ON Encuesta(departamento)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_fecha_evaluacion ON Encuesta(fecha_evaluacion)
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
            print("Base de datos inicializada correctamente")
            return True
        else:
            print("No se pudo inicializar la base de datos")
            return False
    
    @staticmethod
    def guardar_evaluacion(datos):
        """Guarda los datos de evaluación en la base de datos"""
        conn = Database.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Insertar datos en la tabla Encuesta
                sql = """
                    INSERT INTO Encuesta (
                        empleado_id, nombre, departamento, fecha_evaluacion,
                        salud, carrera, finanzas, relaciones,
                        crecimiento, ocio, entorno, proposito,
                        objetivos, apoyo
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                values = (
                    datos['empleado_id'], datos['nombre'], datos['departamento'], 
                    datos['fecha_evaluacion'], datos['salud'], datos['carrera'], 
                    datos['finanzas'], datos['relaciones'], datos['crecimiento'], 
                    datos['ocio'], datos['entorno'], datos['proposito'], 
                    datos['objetivos'], datos['apoyo']
                )
                
                cursor.execute(sql, values)
                conn.commit()
                inserted_id = cursor.lastrowid
                
                cursor.close()
                conn.close()
                
                print(f"Datos guardados en MySQL. ID: {inserted_id}")
                return inserted_id
            except mysql.connector.Error as err:
                print(f"Error al guardar en MySQL: {err}")
                return None
        else:
            print("No se pudo conectar a la base de datos para guardar los datos")
            return None