from flask import render_template, request, redirect, session, url_for, Blueprint
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_parameter, get_page_args
from . import explorar_bp
from flasgger import Swagger, swag_from




client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
db = client['TFG']
form_collection = db['publicar_duda']




@explorar_bp.route('/explorar', methods=['GET', 'POST'])
@swag_from('../api/explorar.yml')
def explorar():
    logged_user = session.get('logged_user')

    if request.method == 'POST':
        # Verificar si el usuario está autenticado antes de procesar la solicitud POST
        if not logged_user:
            return redirect(url_for('auth.login'))  # Redirigir al inicio de sesión si el usuario no está autenticado

        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')

        # Aplicar filtros si se han seleccionado valores
        filtros = {}
        if carrera:
            filtros['carrera'] = carrera
        if curso:
            filtros['curso'] = curso

        # Consultar las dudas con los filtros aplicados
        dudas = form_collection.find({'titulo': {'$regex': consulta, '$options': 'i'}, **filtros})
    else:
        # Si la solicitud no es POST, mostrar todas las dudas sin filtros
        dudas = form_collection.find()

    # Obtener el número de página actual y la cantidad de elementos por página
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  # Mostrar 9 elementos por página

    # Calcular el desplazamiento para la consulta en la base de datos
    offset = (page - 1) * per_page

    # Consultar las dudas con el límite y desplazamiento adecuados
    dudas = dudas.skip(offset).limit(per_page)

    # Obtener el total de dudas para la paginación
    total_dudas = form_collection.count_documents({})

    # Crear el objeto de paginación
    pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

    return render_template('explorar.html', dudas=dudas, pagination=pagination, logged_user=logged_user)

