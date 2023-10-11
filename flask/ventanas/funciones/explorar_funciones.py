
from pymongo import MongoClient


def obtener_dudas(consulta, carrera, curso, imagen, page, per_page):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    if per_page <= 0:
        raise ValueError("per_page debe ser un valor positivo")

    filtros = {
        'titulo': {'$regex': consulta, '$options': 'i'},
    }

    if carrera:
        filtros['carrera'] = carrera
    if curso:
        filtros['curso'] = curso
    
    print(f"Filtros aplicados: {filtros}")  # Agrega este print para ver los filtros aplicados
    total_dudas = form_collection.count_documents(filtros)
    print(f"Total de dudas antes de la paginación: {total_dudas}")  # Agrega este print para ver el total de dudas antes de la paginación
    offset = (page - 1) * per_page
    dudas = form_collection.find(filtros).skip(offset).limit(per_page)
    resultados = []
    for duda in dudas:
        parametros_duda = {
            'titulo': duda.get('titulo', ''),
            'descripcion': duda.get('descripcion', ''),
            'carrera': duda.get('carrera', ''),
            'curso': duda.get('curso', ''),
            'imagen': duda.get('imagen', '')
        }
        resultados.append(parametros_duda)

    print(f"Total de dudas después de la paginación: {len(resultados)}")  # Agrega este print para ver el total de dudas después de la paginación
    return resultados





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

