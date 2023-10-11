
from pymongo import MongoClient

def obtener_dudas(consulta, carrera, curso,imagen, page, per_page):
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

    dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, 'carrera': carrera, 'curso': curso, 'imagen': imagen})
    total_dudas = dudas.count()
    offset = (page - 1) * per_page
    dudas = dudas.skip(offset).limit(per_page)
    
    resultados = []
    for duda in dudas:
        parametros_duda = {
            'titulo': duda.get('titulo', ''),
            'descripcion': duda.get('descripcion', ''),
            'carrera': duda.get('carrera', ''),
            'curso': duda.get('curso', ''),
            'imagen': duda.get('imagen', '')
            # Agrega otros campos si es necesario
        }
        resultados.append(parametros_duda)

    return resultados, total_dudas


def obtener_parametros_dudas():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    dudas = form_collection.find()
    parametros_dudas = []

    for duda in dudas:
        parametros_duda = {
            'titulo': duda.get('titulo', ''),
            'descripcion': duda.get('texto', ''),
            'carrera': duda.get('carrera', ''),
            'curso': duda.get('curso', ''),
            'imagen': duda.get('imagen', '')
        }
        parametros_dudas.append(parametros_duda)

    return parametros_dudas
