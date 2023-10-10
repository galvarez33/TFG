from pymongo import MongoClient
from bson import ObjectId

# Define una variable global para la conexión a la base de datos
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']

# Función para conectar a la base de datos
def conectar_db():
    return form_collection

# Función para obtener las dudas de un usuario
def obtener_dudas_usuario(correo_usuario, page=1, per_page=9):
    offset = (page - 1) * per_page
    dudas = form_collection.find({'correo_usuario': correo_usuario}).skip(offset).limit(per_page)
    return dudas

# Función para borrar una duda por su ID
def borrar_duda_por_id(duda_id):
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})
    if duda:
        form_collection.delete_one({'_id': ObjectId(duda_id)})

def obtener_total_dudas_usuario(correo_usuario):
    total_dudas_usuario = form_collection.count_documents({'correo_usuario': correo_usuario})
    return total_dudas_usuario

def obtener_total_votos(correo_usuario):
    total_votos_positivos = 0
    total_votos_negativos = 0

    dudas = form_collection.find({'comentario.correo': correo_usuario})

    for duda in dudas:
        comentarios = duda.get('comentario', [])
        for comentario in comentarios:
            comentario_votos_positivos = comentario.get('votos_positivos', 0)
            comentario_votos_negativos = comentario.get('votos_negativos', 0)
            total_votos_positivos += comentario_votos_positivos
            total_votos_negativos += comentario_votos_negativos

    return total_votos_positivos, total_votos_negativos


