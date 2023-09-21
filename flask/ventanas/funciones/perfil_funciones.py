from pymongo import MongoClient
from bson import ObjectId

# Función para conectar a la base de datos
def conectar_db():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    return form_collection

# Función para obtener las dudas de un usuario
def obtener_dudas_usuario(correo_usuario):
    form_collection = conectar_db()
    dudas = form_collection.find({'correo_usuario': correo_usuario})
    return dudas

# Función para borrar una duda por su ID
def borrar_duda_por_id(duda_id):
    form_collection = conectar_db()
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})
    if duda:
        form_collection.delete_one({'_id': ObjectId(duda_id)})

        from pymongo import MongoClient

def obtener_total_dudas_usuario(correo_usuario):
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']

    # Contar el total de dudas del usuario
    total_dudas_usuario = form_collection.count_documents({'correo_usuario': correo_usuario})

    return total_dudas_usuario

