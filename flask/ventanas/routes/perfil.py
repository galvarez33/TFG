from flask import render_template, request, redirect, session, url_for, Blueprint
from flask_paginate import Pagination, get_page_args
from . import perfil_bp
from funciones.perfil_funciones import obtener_dudas_usuario, obtener_total_dudas_usuario, borrar_duda_por_id, obtener_total_votos
import requests

from . import perfil_bp

@perfil_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():

    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'
    
    correo_usuario = logged_user['correo']

    if request.method == 'POST':
        consulta = request.form.get('consulta', '')
        carrera = request.form.get('carrera', '')
        curso = request.form.get('curso', '')
        imagen = request.form.get('imagen', '')  
        api_url = f'http://localhost:5001/api/perfil/{correo_usuario}' 

        response = requests.post(api_url, json={'consulta': consulta, 'carrera': carrera, 'curso': curso, 'imagen': imagen})
        if response.status_code == 200:
            data = response.json()
            dudas = data.get('dudas', [])
        else:
            return 'Error al obtener datos del servidor', 500
        data = response.json()
        dudas = data.get('dudas', [])

        
        response_all = requests.get(api_url)
        data_all = response_all.json().get('dudas', [])

        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 9 
        start = (page - 1) * per_page
        end = start + per_page

        dudas_paginadas = dudas[start:end]
        total_dudas = len(dudas) 

        pagination = Pagination(page=page, per_page=per_page, total=total_dudas, css_framework='bootstrap4')

        return render_template('perfil.html', dudas=dudas_paginadas, pagination=pagination, logged_user=logged_user)

    # Hacer una solicitud HTTP a la API para obtener los datos del perfil del usuario
    api_url = f'http://localhost:5001/api/perfil/{correo_usuario}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()  # Los datos del perfil del usuario se encuentran en el formato JSON de la respuesta
        dudas_usuario = data.get('dudas', [])
        total_votos_positivos = data.get('total_votos_positivos', 0)
        total_votos_negativos = data.get('total_votos_negativos', 0)
    else:
        # Manejar el caso cuando la solicitud a la API no es exitosa
        dudas_usuario = []
        total_votos_positivos = 0
        total_votos_negativos = 0

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9

    offset = (page - 1) * per_page
    dudas_usuario = dudas_usuario[offset: offset + per_page]
    total_dudas_usuario = len(dudas_usuario)

    pagination = Pagination(page=page, per_page=per_page, total=total_dudas_usuario, css_framework='bootstrap4')

    return render_template('perfil.html', dudas=dudas_usuario, pagination=pagination, logged_user=logged_user, total_votos_positivos=total_votos_positivos, total_votos_negativos=total_votos_negativos)


@perfil_bp.route('/borrar_duda', methods=['POST'])
def borrar_duda():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    correo_usuario = logged_user['correo']
    duda_id = request.form.get('duda_id')  


    if duda_id:
        api_url = f'http://localhost:5001/api/perfil/{correo_usuario}'
        response = requests.delete(api_url, json={'duda_id': duda_id})  

        if response.status_code == 200:
            return redirect(url_for('perfil.perfil'))
        else:
            return 'Error al borrar la duda', 500
    else:
        return 'ID de duda inválido', 400
