
from pymongo import MongoClient

def obtener_dudas(consulta, carrera, curso, page, per_page):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    if per_page <= 0:
        raise ValueError("per_page debe ser un valor positivo")

    filtros = {}
    if carrera:
        filtros['carrera'] = carrera
    if curso:
        filtros['curso'] = curso

    dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, **filtros})
    offset = (page - 1) * per_page
    dudas = dudas.skip(offset).limit(per_page)
    total_dudas = form_collection.count_documents({})
    return dudas, total_dudas


def obtener_parametros_dudas():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    dudas = form_collection.find()

    parametros_dudas = []

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
