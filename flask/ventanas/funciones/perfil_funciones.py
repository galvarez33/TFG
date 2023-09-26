from pymongo import MongoClient
from bson import ObjectId

# Función para conectar a la base de datos
def conectar_db():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    return form_collection

# Función para obtener las dudas de un usuario
def obtener_dudas_usuario(correo_usuario, page=1, per_page=9):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    offset = (page - 1) * per_page
    dudas = form_collection.find({'correo_usuario': correo_usuario}).skip(offset).limit(per_page)
    
    return dudas



# Función para borrar una duda por su ID
def borrar_duda_por_id(duda_id):
    form_collection = conectar_db()
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})
    if duda:
        form_collection.delete_one({'_id': ObjectId(duda_id)})

def obtener_total_dudas_usuario(correo_usuario):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    # Contar el total de dudas del usuario
    total_dudas_usuario = form_collection.count_documents({'correo_usuario': correo_usuario})

    return total_dudas_usuario

def obtener_total_votos_positivos(correo_usuario):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    comentarios_collection = db['publicar_duda']  # Cambia el nombre de la colección a la de tus comentarios

    # Inicializa una variable para almacenar el total de votos positivos
    total_votos_positivos = 0

    # Consulta los comentarios del usuario
    dudas = comentarios_collection.find({'comentario.correo': correo_usuario})

    # Itera a través de las dudas
    for duda in dudas:
        comentarios = duda.get('comentario', [])  # Obtén la lista de comentarios de la duda
        for comentario in comentarios:
            # Dentro del comentario, busca el campo 'votos_positivos'
            comentario_votos_positivos = comentario.get('votos_positivos', 0)
            total_votos_positivos += comentario_votos_positivos

    return total_votos_positivos


