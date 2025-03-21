from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from config.config import Config
from config.db import Database
from config.data_handler import DataHandler

# Crear la aplicación Flask
app = Flask(__name__, 
            static_folder='.',  # Para servir archivos estáticos desde la raíz
            template_folder='templates')  # Carpeta para los templates HTML

# Cargar configuración
app.config.from_object(Config)
Config.init_app(app)

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/evaluacion', methods=['GET'])
def evaluacion():
    return render_template('evaluacion.html')

@app.route('/procesar_evaluacion', methods=['POST'])
def procesar_evaluacion():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            datos = {
                'empleado_id': request.form['empleado_id'],
                'nombre': request.form['nombre'],
                'departamento': request.form['departamento'],
                'fecha_evaluacion': request.form['fecha'],
                'salud': int(request.form['salud']),
                'carrera': int(request.form['carrera']),
                'finanzas': int(request.form['finanzas']),
                'relaciones': int(request.form['relaciones']),
                'crecimiento': int(request.form['crecimiento']),
                'ocio': int(request.form['ocio']),
                'entorno': int(request.form['entorno']),
                'proposito': int(request.form['proposito']),
                'objetivos': request.form['objetivos'],
                'apoyo': request.form['apoyo'],
                'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Guardar en CSV
            csv_file = DataHandler.guardar_csv(datos)
            
            # Guardar en JSON
            json_file = DataHandler.guardar_json(datos)
            
            # Guardar en MySQL
            db_id = Database.guardar_evaluacion(datos)
            
            if db_id:
                flash('¡Evaluación registrada correctamente!', 'success')
            else:
                flash('La evaluación se guardó en archivos pero no en la base de datos', 'warning')
                
            return redirect(url_for('evaluacion'))
        except Exception as e:
            flash(f'Error al procesar la evaluación: {str(e)}', 'error')
            print(f"Error: {str(e)}")
            return redirect(url_for('evaluacion'))

# Ruta para mostrar un mensaje de confirmación
@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')

if __name__ == '__main__':
    # Inicializar la base de datos al iniciar la aplicación
    Database.init_db()
    
    # Ejecutar la aplicación Flask en modo de desarrollo
    app.run(debug=True)