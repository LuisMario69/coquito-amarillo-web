from flask import Flask, render_template, jsonify, request
from config.config import Config
from app.models import RuedaVida
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    app.config.from_object(Config)
    
    @app.route('/')
    def index():
        preguntas = RuedaVida.get_preguntas()
        return render_template('index.html', preguntas=preguntas)
    
    @app.route('/guardar_respuesta', methods=['POST'])
    def guardar_respuesta():
        data = request.json
        categoria = data.get('categoria')
        valor = data.get('valor')

        logger.debug(f"Recibida respuesta - Categoria: {categoria}, Valor: {valor}")

        # Guardar respuesta individual
        success = RuedaVida.guardar_respuesta(categoria, valor)
        logger.debug(f"Guardado de respuesta: {success}")

        # Obtener todos los datos
        datos = RuedaVida.get_all_data()
        logger.debug(f"Datos obtenidos: {datos}")
        
        if datos:
            df = pd.DataFrame(datos)
            
            # Generar gráfica de radar
            fig = px.line_polar(
                df, 
                r='valor', 
                theta='categoria', 
                line_close=True,
                title='Rueda de la Vida',
                range_r=[0, 10]
            )
            
            fig.update_traces(fill='toself')
            
            grafica_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
            logger.debug("Gráfica generada correctamente")
            
            return jsonify({"success": success, "grafica": grafica_html})
        else:
            logger.warning("No se encontraron datos para generar la gráfica")
            return jsonify({"success": success, "grafica": "No hay datos"})
    
    return app