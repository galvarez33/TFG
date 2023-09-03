from flask import render_template, request, redirect, session, url_for, Blueprint
from pymongo import MongoClient
from bson import ObjectId
from flask_paginate import Pagination, get_page_args  # Asegúrate de tener Flask-Paginate instalado
from . import perfil_bp



# Conectar a la base de datos MongoDB (esto puede ir en tu archivo main.py)
client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']

# Ruta para ver el perfil del usuario
@perfil_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    # Obtener el correo del usuario logueado desde la sesión
    usuario_correo = logged_user['correo']

    if request.method == 'POST':
        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')

        # Aplicar filtros si se han seleccionado valores
        filtros = {
            'correo_usuario': usuario_correo  # Agregar filtro por correo del usuario
        }
        if carrera:
            filtros['carrera'] = carrera
        if curso:
            filtros['curso'] = curso

        # Consultar las dudas del usuario con los filtros aplicados
        dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, **filtros})
    else:
        # Si la solicitud no es POST, mostrar todas las dudas del usuario sin filtros
        dudas = form_collection.find({'correo_usuario': usuario_correo})

    # Obtener el número de página actual y la cantidad de elementos por página
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  # Mostrar 9 elementos por página

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page

    # Consultar las dudas del usuario con el límite y desplazamiento adecuados
    dudas = dudas.skip(offset).limit(per_page)

    # Obtener el total de dudas del usuario para la paginación
    total_dudas = form_collection.count_documents({'correo_usuario': usuario_correo})

    # Crear el objeto de paginación
    pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

    return render_template('perfil.html', dudas=dudas, pagination=pagination, logged_user=logged_user)

# Ruta para borrar una duda del usuario
@perfil_bp.route('/borrar_duda/<string:duda_id>', methods=['POST'])
def borrar_duda(duda_id):
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    # Obtener la duda desde la base de datos
    duda = form_collection.find_one({'_id': ObjectId(duda_id)})

    if duda:
        # Verificar si el usuario logueado es el propietario de la duda
        if duda.get('correo_usuario') == logged_user['correo']:
            # Borrar la duda de la base de datos
            form_collection.delete_one({'_id': ObjectId(duda_id)})

    return redirect(url_for('perfil.perfil'))  # Ajusta la redirección al perfil en Blueprint



