from flask import render_template, request, redirect, session, url_for, Blueprint
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_parameter, get_page_args
from . import explorar_bp
from flasgger import Swagger, swag_from
from funciones.explorar_funciones import obtener_dudas
import requests



@explorar_bp.route('/explorar', methods=['GET', 'POST'])
def explorar():
    logged_user = session.get('logged_user')

    if request.method == 'POST':
        
        # Verificar si el usuario está autenticado antes de procesar la solicitud POST
        if not logged_user:
            return redirect(url_for('auth.login'))  # Redirigir al inicio de sesión si el usuario no está autenticado

        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')
    else:
        consulta = ''
        carrera = ''
        curso = ''

    api_url = 'http://localhost:5001/api/explorar'  # Reemplaza con la URL de tu API
    response = requests.get(api_url)
    data = response.json().get('dudas', [])

    # Paginación
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9  # Mostrar 9 elementos por página
    start = (page - 1) * per_page
    end = start + per_page

    dudas = data[start:end]
    total_dudas = len(data)

    pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

    return render_template('explorar.html', dudas=dudas, pagination=pagination, logged_user=logged_user)
