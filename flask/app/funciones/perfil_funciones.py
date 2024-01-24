from pymongo import MongoClient
from bson import ObjectId
import base64

# Define una variable global para la conexión a la base de datos
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']

# Función para conectar a la base de datos
def conectar_db():
    return form_collection

# Función para obtener las dudas de un usuario
def obtener_dudas_usuario(correo_usuario, consulta=None, carrera=None, curso=None, page=1, per_page=9):
    
    query = {'correo_usuario': correo_usuario}
    
    if consulta:
        query['$or'] = [
            {'titulo': {'$regex': consulta, '$options': 'i'}},
            {'texto': {'$regex': consulta, '$options': 'i'}}
        ]

    if carrera:
        query['carrera'] = carrera

    if curso:
        query['curso'] = curso
    
    offset = (page - 1) * per_page
    dudas_cursor = form_collection.find(query).skip(offset).limit(per_page)
    
    # Convertir ObjectId a cadena y crear la lista de dudas
    dudas = [
        {
            '_id': str(duda['_id']),  # Convertir ObjectId a cadena
            'titulo': duda.get('titulo', ''),
            'descripcion': duda.get('texto', ''),
            'imagen': duda.get('imagen', '')
        }
        for duda in dudas_cursor
    ]
    
    return dudas


def borrar_duda_por_id(duda_id, correo_usuario):
    duda = form_collection.find_one({'_id': ObjectId(duda_id), 'correo_usuario': correo_usuario})
    if duda:
        form_collection.delete_one({'_id': ObjectId(duda_id), 'correo_usuario': correo_usuario})
        return True
    else:
        return False


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

def conectar_db_usuarios():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    usuarios_collection = db['usuarios']  # Cambiar a la colección de usuarios
    return usuarios_collection

def guardar_imagen_perfil_en_bd(correo, nueva_imagen):
    usuarios_collection = conectar_db_usuarios()

    # Convertir la imagen a base64
    imagen_base64 = base64.b64encode(nueva_imagen.read()).decode('utf-8')

    # Actualizar el documento del usuario en la base de datos con la nueva imagen en base64
    usuarios_collection.update_one(
        {'correo': correo},
        {'$set': {'imagen_perfil': imagen_base64}}
    )


def obtener_imagen_perfil_desde_bd(correo_usuario):
    # Realizar una consulta a la base de datos para obtener la imagen de perfil del usuario
    collection = conectar_db_usuarios()
    usuario = collection.find_one({'correo': correo_usuario})

    if usuario and 'imagen_perfil' in usuario:
        return usuario['imagen_perfil']
    else:
        return None