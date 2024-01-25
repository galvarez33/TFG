from flask import render_template, request, redirect, session, url_for, Blueprint,jsonify
from flask_paginate import Pagination, get_page_args
from . import perfil_bp
from funciones.perfil_funciones import obtener_dudas_usuario, obtener_total_dudas_usuario, borrar_duda_por_id, obtener_total_votos, guardar_imagen_perfil_en_bd
import requests
import base64
import json

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
        api_url = f'http://localhost/api/perfil/{correo_usuario}' 
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
    api_url = f'http://localhost/api/perfil/{correo_usuario}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json() 
        # Los datos del perfil del usuario se encuentran en el formato JSON de la respuesta
        dudas_usuario = data.get('dudas', [])
        total_votos_positivos = data.get('total_votos_positivos', 0)
        
        total_votos_negativos = data.get('total_votos_negativos', 0)
        imagen_perfil = data.get('imagen_perfil', '') 
    else:
        # Manejar el caso cuando la solicitud a la API no es exitosa
        dudas_usuario = []
        total_votos_positivos = 0
        total_votos_negativos = 0
        imagen_perfil = '' 


    api_url_ranking = f'http://localhost/api/ranking/{correo_usuario}'
    response_ranking = requests.get(api_url_ranking)

    if response_ranking.status_code == 200:
        posicion_ranking = response_ranking.json().get('posicion', None)
        puntos_ranking = response_ranking.json().get('puntos', 0)
    else:
        # Manejar el caso cuando la solicitud a la API de ranking no es exitosa
        posicion_ranking = None
        puntos_ranking = 0

    # Ahora puedes usar 'posicion_ranking' y 'puntos_ranking' en tu código según sea necesario



    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 9

    offset = (page - 1) * per_page
    dudas_usuario = dudas_usuario[offset: offset + per_page]
    total_dudas_usuario = len(dudas_usuario)

    pagination = Pagination(page=page, per_page=per_page, total=total_dudas_usuario, css_framework='bootstrap4')

    return render_template('perfil.html', dudas=dudas_usuario, imagen_perfil=imagen_perfil,pagination=pagination,posicion_ranking=posicion_ranking,puntos_ranking=puntos_ranking, logged_user=logged_user, total_votos_positivos=total_votos_positivos, total_votos_negativos=total_votos_negativos)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@perfil_bp.route('/cambiar_imagen_perfil', methods=['POST'])
def cambiar_imagen_perfil():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    correo_usuario = logged_user['correo']

    # Obtén el archivo de la solicitud del formulario
    nueva_imagen = request.files['nuevaImagen']

    # Verifica si el archivo tiene una extensión permitida
    if not allowed_file(nueva_imagen.filename):
        return 'Error: formato de archivo no permitido. Por favor, elige una imagen válida.', 400

    # Llama a la función para guardar la imagen de perfil en la base de datos
    guardar_imagen_perfil_en_bd(correo_usuario, nueva_imagen)

    # Hacer una solicitud HTTP a la API para actualizar la información del perfil
    api_url = f'http://localhost/api/perfil/{correo_usuario}'
    consulta = request.form.get('consulta', '')
    carrera = request.form.get('carrera', '')
    curso = request.form.get('curso', '')

    imagen_base64 = base64.b64encode(nueva_imagen.read()).decode('utf-8')

    response = requests.post(api_url, json={'consulta': consulta, 'carrera': carrera, 'curso': curso, 'imagen_perfil': imagen_base64})

    if response.status_code == 200:
        # Redirige a la página del perfil después de cambiar la imagen
        return redirect(url_for('perfil.perfil'))
    else:
        return 'Error al actualizar la imagen de perfil', 500



@perfil_bp.route('/borrar_duda', methods=['POST'])
def borrar_duda():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    correo_usuario = logged_user['correo']
    duda_id = request.form.get('duda_id')  


    if duda_id:
        api_url = f'http://localhost/api/perfil/{correo_usuario}'
        response = requests.delete(api_url, json={'duda_id': duda_id})  

        if response.status_code == 200:
            return redirect(url_for('perfil.perfil'))
        else:
            return 'Error al borrar la duda', 500
    else:
        return 'ID de duda inválido', 400


@perfil_bp.route('/obtener_ranking', methods=['GET'])
def obtener_ranking():
    try:
        with open('ranking.json', 'r') as file:
            ranking_data = json.load(file)
        return jsonify(ranking_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify(error='Error al cargar los datos del ranking')

@perfil_bp.route('/borrar_imagen_perfil', methods=['POST'])
def borrar_imagen_perfil():
    logged_user = session.get('logged_user')
    if not logged_user:
        return 'Acceso no autorizado'

    correo_usuario = logged_user['correo']

    api_url = f'http://localhost/api/perfil/{correo_usuario}'
    
    # Incluye el parámetro 'borrar_imagen_perfil' en el cuerpo de la solicitud DELETE
    payload = {'borrar_imagen_perfil': True}
    
    response = requests.delete(api_url, json=payload)

    if response.status_code == 200:
        # Redirige a la página del perfil después de borrar la imagen
        return redirect(url_for('perfil.perfil'))
    else:
        return 'Error al borrar la imagen de perfil', 500
