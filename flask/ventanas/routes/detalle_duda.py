from flask import render_template, request, redirect, session, url_for, Blueprint
from pymongo import MongoClient
from datetime import datetime
import base64
from bson import ObjectId
from . import detalle_duda_bp



# Conectar a la base de datos MongoDB (esto puede ir en tu archivo main.py)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']

# Ruta para ver los detalles de una duda
@detalle_duda_bp.route('/detalle_duda/<duda_id>', methods=['GET', 'POST'])
def detalle_duda(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return redirect(url_for('auth.login'))  # Redirigir al inicio de sesión si el usuario no está autenticado

    nombre_usuario = session.get('nombre_usuario')

    duda = obtener_detalle_duda(duda_id)

    if duda:
        for comentario in duda['comentario']:
            comentario['votos_positivos_count'] = comentario.get('votos_positivos', 0)

        if request.method == 'POST':
            nuevo_comentario = request.form.get('comentario')
            imagen = request.files['imagen']

            if imagen:
                imagen_base64 = base64.b64encode(imagen.read()).decode('utf-8')
            else:
                imagen_base64 = None

            # Crear la tupla de comentario e imagen
            comentario_con_imagen = {
                'nombre': nombre_usuario,
                'texto': nuevo_comentario,
                'imagen': imagen_base64,
                'votos_positivos': 0,
                'votos_negativos': 0,
                'fecha_agregado': datetime.now()  # Agrega la fecha de agregado
            }

            form_collection.update_one(
                {'_id': duda['_id']},
                {'$push': {'comentario': comentario_con_imagen}}
            )

            return redirect(url_for('detalle_duda.detalle_duda', duda_id=duda['_id']))

        comentario_index = request.args.get('comentario_index')
        if comentario_index is not None:
            comentario_index = int(comentario_index)
            form_collection.update_one(
                {'_id': duda['_id']},
                {'$unset': {f'comentario.{comentario_index}': 1}}
            )
            form_collection.update_one(
                {'_id': duda['_id']},
                {'$pull': {'comentario': None}}
            )
            return redirect(url_for('detalle_duda.detalle_duda', duda_id=duda['_id']))

        orden = request.args.get('orden')
        if orden == 'mejor_votados':
            duda['comentario'].sort(key=lambda x: x['votos_positivos'], reverse=True)
        elif orden == 'recientes':
            duda['comentario'].sort(key=lambda x: x['fecha_agregado'], reverse=True)

        return render_template('detalle_duda.html', duda=duda, logged_user=logged_user, nombre_usuario=nombre_usuario)
    else:
        return render_template('error.html', mensaje='Duda no encontrada')

# Función para obtener los detalles de una duda por su ID
def obtener_detalle_duda(duda_id):
    # Convertir el duda_id a ObjectId
    object_id = ObjectId(duda_id)
    duda = form_collection.find_one({'_id': object_id})

    return duda



@detalle_duda_bp.route('/votar_positivo/<string:duda_id>/<int:comentario_index>', methods=['POST'])
def votar_positivo(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    nombre_usuario = session.get('nombre_usuario')

    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        comentarios = duda.get('comentario', [])

        if 0 <= comentario_index < len(comentarios):
            comentario = comentarios[comentario_index]

            # Verifica si el usuario ya ha votado en este comentario
            usuario_voto = nombre_usuario
            if usuario_voto not in comentario.get('usuarios_votados', []):
                comentario['votos_positivos'] += 1
                comentario.setdefault('usuarios_votados', []).append(usuario_voto)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )

        return redirect(url_for('detalle_duda.detalle_duda', duda_id=duda_id))

    return 'Acceso no autorizado'



@detalle_duda_bp.route('/votar_negativo/<string:duda_id>/<int:comentario_index>', methods=['POST'])
def votar_negativo(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    nombre_usuario = session.get('nombre_usuario')

    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        comentarios = duda.get('comentario', [])

        if 0 <= comentario_index < len(comentarios):
            comentario = comentarios[comentario_index]

            # Verifica si el usuario ya ha votado en este comentario
            usuario_voto = nombre_usuario
            if usuario_voto not in comentario.get('usuarios_votados', []):
                comentario['votos_negativos'] += 1
                comentario.setdefault('usuarios_votados', []).append(usuario_voto)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )

        return redirect(url_for('detalle_duda.detalle_duda', duda_id=duda_id))

    return 'Acceso no autorizado'







@detalle_duda_bp.route('/borrar_comentario/<duda_id>/<int:comentario_index>', methods=['POST'])
def borrar_comentario(duda_id, comentario_index):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    nombre_usuario = session.get('nombre_usuario')

    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        comentarios = duda.get('comentario', [])

        if 0 <= comentario_index < len(comentarios):
            if nombre_usuario == comentarios[comentario_index]['nombre']:
                comentarios.pop(comentario_index)

                form_collection.update_one(
                    {'_id': duda['_id']},
                    {'$set': {'comentario': comentarios}}
                )

        return redirect(url_for('detalle_duda.detalle_duda', duda_id=duda_id))

    return 'Acceso no autorizado'
