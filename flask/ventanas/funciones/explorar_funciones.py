# funciones/explorar_funciones.py
from pymongo import MongoClient

def obtener_dudas(consulta, carrera, curso, page, per_page):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    filtros = {}
    if carrera:
        filtros['carrera'] = carrera
    if curso:
        filtros['curso'] = curso

    dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, **filtros})

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page

    # Consultar las dudas con el límite y desplazamiento adecuados
    dudas = dudas.skip(offset).limit(per_page)

    # Obtener el total de dudas para la paginación
    total_dudas = form_collection.count_documents({})


    return dudas, total_dudas


def obtener_parametros_dudas():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    # Aquí realiza la consulta para obtener las dudas de la base de datos
    dudas = form_collection.find()

    # Inicializa una lista para almacenar los parámetros de las dudas
    parametros_dudas = []

    # Recorre las dudas y almacena los parámetros en la lista
    for duda in dudas:
        parametros_duda = {
            'titulo': duda.get('titulo', ''),  # Usa get para manejar claves faltantes
            'descripcion': duda.get('descripcion', ''),  # Usa get para manejar claves faltantes
            'carrera': duda.get('carrera', ''),  # Usa get para manejar claves faltantes
            'curso': duda.get('curso', ''),  # Usa get para manejar claves faltantes
            # Agrega otros campos si es necesario
        }
        parametros_dudas.append(parametros_duda)

    return parametros_dudas
