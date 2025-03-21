import os
import csv
import json
from datetime import datetime
from config.config import Config

class DataHandler:
    @staticmethod
    def guardar_csv(datos):
        """Guarda los datos en un archivo CSV"""
        # Generar nombre de archivo con fecha actual
        filename = os.path.join(
            Config.CSV_DIR, 
            f"evaluaciones_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        # Verificar si el archivo ya existe
        file_exists = os.path.isfile(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'empleado_id', 'nombre', 'departamento', 'fecha_evaluacion', 
                'salud', 'carrera', 'finanzas', 'relaciones', 
                'crecimiento', 'ocio', 'entorno', 'proposito', 
                'objetivos', 'apoyo', 'fecha_registro'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escribir encabezados si el archivo es nuevo
            if not file_exists:
                writer.writeheader()
            
            # Escribir los datos
            writer.writerow(datos)
        
        print(f"Datos guardados en CSV: {filename}")
        return filename
    
    @staticmethod
    def guardar_json(datos):
        """Guarda los datos en un archivo JSON"""
        # Generar nombre de archivo con fecha actual
        filename = os.path.join(
            Config.JSON_DIR, 
            f"evaluaciones_{datetime.now().strftime('%Y%m%d')}.json"
        )
        
        # Leer datos existentes si el archivo existe
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as jsonfile:
                try:
                    existing_data = json.load(jsonfile)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        # Añadir nuevos datos
        existing_data.append(datos)
        
        # Guardar todos los datos
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(existing_data, jsonfile, indent=4, ensure_ascii=False)
        
        print(f"Datos guardados en JSON: {filename}")
        return filename