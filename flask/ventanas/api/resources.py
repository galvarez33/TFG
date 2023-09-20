# api/resources.py

from flask_restful import Resource
from funciones.explorar_funciones import obtener_parametros_dudas

class ExplorarResource(Resource):
    def get(self):
        # Llama a la función obtener_parametros_dudas para obtener los parámetros de las dudas
        parametros_dudas = obtener_parametros_dudas()

        # Convierte los parámetros de las dudas en una respuesta JSON
        return {'dudas': parametros_dudas}
