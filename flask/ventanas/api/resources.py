from flask_restful import Resource
from routes.explorar import explorar  # Asegúrate de que la importación sea correcta

class ExplorarResource(Resource):
    def get(self):
        # Llamar a la función explorar() para obtener los datos
        dudas = explorar()
        
        
        # Convertir los datos a un formato JSON adecuado
        result = []
        for duda in dudas:
            duda_json = {
                'titulo': duda['titulo'],
                'descripcion': duda['descripcion'],
                'carrera': duda['carrera'],
                'curso': duda['curso'],
                # Agregar otros campos si es necesario
            }
            result.append(duda_json)
        
        print(result)
        return {'dudas': result}