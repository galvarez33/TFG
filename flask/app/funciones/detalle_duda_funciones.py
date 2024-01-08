from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import base64
import json

# Conectar a la base de datos
def conectar_db():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']
    form_collection = db['publicar_duda']
    notificaciones_collection = db['notificaciones']  
    return form_collection, notificaciones_collection


# Función para obtener los detalles de una duda por su ID
def obtener_detalle_duda(duda_id):
    form_collection, _ = conectar_db()
    object_id = ObjectId(duda_id)
    duda = form_collection.find_one({'_id': object_id})
    
    return duda



def agregar_comentario(duda_id, comentario):
    form_collection, notificaciones_collection = conectar_db()
    
    
    duda = obtener_detalle_duda(duda_id)
    if not duda:
        return False  

    imagen_data = comentario.get('imagen_data')
    if imagen_data:
        imagen_base64 = base64.b64encode(imagen_data).decode('utf-8')
        comentario['imagen'] = imagen_base64
        del comentario['imagen_data']

    if form_collection.update_one(
        {'_id': duda['_id']},
        {'$push': {'comentario': comentario}}
    ):
        
        notificacion = {
            'duda_id': duda['_id'],
            'correo_usuario_duda': duda.get('correo_usuario', ''),  
            'nombre_usuario_comentario': comentario['nombre'],  
            'asignatura': duda.get('asignatura', ''),  
            'fecha': datetime.now()
        }
        notificaciones_collection.insert_one(notificacion)
        return True
    else:
        return False

# Función para votar positivamente un comentario
def votar_positivo_comentario(ranking_file_path, duda_id, comentario_index, usuario_voto):
    form_collection, notificaciones_collection = conectar_db()
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        comentarios = duda.get('comentario', [])

        if 0 <= comentario_index < len(comentarios):
            comentario = comentarios[comentario_index]

            if usuario_voto not in comentario.get('usuarios_votados', []):
                comentario['votos_positivos'] += 1
                comentario.setdefault('usuarios_votados', []).append(usuario_voto)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )
                correo_comentario = comentario.get('correo')
                
                ranking_dict = load_ranking_from_file(ranking_file_path)
                
                if correo_comentario in ranking_dict:
                    ranking_dict[correo_comentario]['puntos'] = max(0, ranking_dict[correo_comentario]['puntos'] + 10)
                    guardar_ranking_en_archivo(ranking_file_path, ranking_dict)

# Función para votar negativamente un comentario
def votar_negativo_comentario(ranking_file_path, duda_id, comentario_index, usuario_voto):
    form_collection, notificaciones_collection = conectar_db()
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        comentarios = duda.get('comentario', [])

        if 0 <= comentario_index < len(comentarios):
            comentario = comentarios[comentario_index]

            if usuario_voto not in comentario.get('usuarios_votados', []):
                # Resta un punto solo cuando se vota negativo
                comentario['votos_negativos'] += 1
                comentario.setdefault('usuarios_votados', []).append(usuario_voto)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )

                # Actualiza la puntuación solo si el voto es negativo
                correo_comentario = comentario.get('correo')
                
                ranking_dict = load_ranking_from_file(ranking_file_path)
                
                if correo_comentario in ranking_dict:
                    ranking_dict[correo_comentario]['puntos'] = max(0, ranking_dict[correo_comentario]['puntos'] - 5)
                    guardar_ranking_en_archivo(ranking_file_path, ranking_dict)


def load_ranking_from_file(ranking_file_path):
    try:
        with open(ranking_file_path, 'r') as file:
            # Carga el contenido del archivo JSON y devuelve el diccionario
            ranking_data = json.load(file)
            return ranking_data
    except FileNotFoundError:
        # Si el archivo no existe, devuelve un diccionario vacío
        return {}


def guardar_ranking_en_archivo(ranking_file_path, ranking_dict):
    with open(ranking_file_path, 'w') as file:
        # Guarda el contenido del ranking en el archivo JSON
        json.dump(ranking_dict, file, indent=4)


                   

# Función para borrar un comentario
def borrar_comentario(duda_id, comentario_index):
    try:
        form_collection, _ = conectar_db()  

        duda = form_collection.find_one({'_id': ObjectId(duda_id)})

        if duda:
            comentarios = duda.get('comentario', [])

            if 0 <= comentario_index < len(comentarios):
                comentarios.pop(comentario_index)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )
                return True
    except Exception as e:
        print(f"Error al borrar el comentario: {str(e)}")
    return False




