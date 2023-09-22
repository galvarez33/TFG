from pymongo import MongoClient
from bson import ObjectId

# Función para conectar a la base de datos
def conectar_db():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    return form_collection

# Función para guardar una nueva duda en la base de datos
def guardar_nueva_duda(data):
    form_collection = conectar_db()
    form_collection.insert_one(data)

# Otras funciones relacionadas con la base de datos (obtener, borrar, actualizar, etc.) pueden ir aquí.
def obtener_ultima_duda():
        form_collection = conectar_db()
        ultima_duda = form_collection.find_one(sort=[('_id', -1)])  # Ordenar por ID descendente para obtener la última duda
        return ultima_duda