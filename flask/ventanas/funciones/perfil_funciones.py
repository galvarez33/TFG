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

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page

    # Obtener las dudas del usuario con paginación
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
    comentarios_collection = db['comentarios']  # Supongo el nombre de la colección de comentarios

    # Utiliza la función `count_documents` para contar los votos positivos en los comentarios del usuario
    total_votos_positivos = comentarios_collection.count_documents({'correo_usuario': correo_usuario, 'voto_positivo': True})

    return total_votos_positivos